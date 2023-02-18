#!/bin/bash
set -euo pipefail

datasette --reload cooking.db
