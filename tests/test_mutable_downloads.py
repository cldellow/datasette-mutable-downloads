from datasette.app import Datasette
import sqlite3
import pytest

@pytest.mark.asyncio
async def test_plugin_is_installed(tmp_path):
    db_name = tmp_path / "mydb.db"
    conn = sqlite3.connect(db_name)
    conn.close()
    datasette = Datasette(
        memory=True,
        files=[db_name]
    )
    response = await datasette.client.get("/-/plugins.json")
    assert response.status_code == 200
    installed_plugins = {p["name"] for p in response.json()}
    assert "datasette-mutable-downloads" in installed_plugins

    response = await datasette.client.get('/mydb.db')
    assert response.status_code == 200

