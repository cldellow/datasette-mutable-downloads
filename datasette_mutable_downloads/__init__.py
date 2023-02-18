import os
import tempfile
import sqlite3
import aiofiles
import aiofiles.os
from datasette import hookimpl
from datasette.views.base import DatasetteError
from datasette.utils import add_cors_headers, tilde_decode
from datasette.utils.asgi import AsgiFileDownload, NotFound, Response, Forbidden


@hookimpl
def startup(datasette):
    from datasette.views.database import DatabaseDownload
    print(DatabaseDownload)
    DatabaseDownload.get = DatabaseDownload_get
    pass

# Based on https://github.com/simonw/datasette/blob/0b4a28691468b5c758df74fa1d72a823813c96bf/datasette/views/database.py#L172-L212,
# but patched to permit retrieving mutable databases.
async def DatabaseDownload_get(self, request):
    database = tilde_decode(request.url_vars["database"])
    await self.ds.ensure_permissions(
        request.actor,
        [
            ("view-database-download", database),
            ("view-database", database),
            "view-instance",
        ],
    )
    try:
        db = self.ds.get_database(route=database)
    except KeyError:
        raise DatasetteError("Invalid database", status=404)
    if db.is_memory:
        raise DatasetteError("Cannot download in-memory databases", status=404)
    if not self.ds.setting("allow_download"):
        raise Forbidden("Database download is forbidden")
    if not db.path:
        raise DatasetteError("Cannot download database", status=404)
    filepath = db.path

    vacuumed_file = None

    if db.is_mutable:
        vacuumed_file = tempfile.NamedTemporaryFile(delete=False, prefix='mydb.', suffix='.db').name
        c = sqlite3.connect(filepath)
        c.execute("VACUUM INTO '{}'".format(vacuumed_file))
        c.close()

    headers = {}
    if self.ds.cors:
        add_cors_headers(headers)
    if db.hash:
        etag = '"{}"'.format(db.hash)
        headers["Etag"] = etag
        # Has user seen this already?
        if_none_match = request.headers.get("if-none-match")
        if if_none_match and if_none_match == etag:
            return Response("", status=304)
    headers["Transfer-Encoding"] = "chunked"

    if not vacuumed_file:
        return AsgiFileDownload(
            filepath,
            filename=os.path.basename(filepath),
            content_type="application/octet-stream",
            headers=headers,
        )

    # Use our hacky version of AsgiFileDownload, which will
    # delete the file on completion.
    return AsgiFileDownloadWithDelete(
        vacuumed_file,
        filename=os.path.basename(filepath),
        content_type="application/octet-stream",
        headers=headers,
    )

class AsgiFileDownloadWithDelete:
    def __init__(
        self,
        filepath,
        filename=None,
        content_type="application/octet-stream",
        headers=None,
    ):
        self.headers = headers or {}
        self.filepath = filepath
        self.filename = filename
        self.content_type = content_type

    async def asgi_send(self, send):
        return await asgi_send_file(
            send,
            self.filepath,
            filename=self.filename,
            content_type=self.content_type,
            headers=self.headers,
        )

async def asgi_start(send, status, headers=None, content_type="text/plain"):
    headers = headers or {}
    # Remove any existing content-type header
    headers = {k: v for k, v in headers.items() if k.lower() != "content-type"}
    headers["content-type"] = content_type
    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": [
                [key.encode("latin1"), value.encode("latin1")]
                for key, value in headers.items()
            ],
        }
    )


async def asgi_send_file(
    send, filepath, filename=None, content_type=None, chunk_size=4096, headers=None
):
    headers = headers or {}
    if filename:
        headers["content-disposition"] = f'attachment; filename="{filename}"'
    first = True
    headers["content-length"] = str((await aiofiles.os.stat(str(filepath))).st_size)
    async with aiofiles.open(str(filepath), mode="rb") as fp:
        if first:
            await asgi_start(
                send,
                200,
                headers,
                content_type or guess_type(str(filepath))[0] or "text/plain",
            )
            first = False
        more_body = True
        while more_body:
            chunk = await fp.read(chunk_size)
            more_body = len(chunk) == chunk_size
            await send(
                {"type": "http.response.body", "body": chunk, "more_body": more_body}
            )

    os.remove(filepath)

@hookimpl
def extra_template_vars(request, datasette, database, view_name):
    if view_name != 'database':
        return {}

    if not datasette.setting('allow_download'):
        return {}

    db = datasette.databases[database]

    if db.is_memory:
        return {}

    return {
        "allow_download": True
    }
