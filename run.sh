#!/bin/bash
python -m pip install -r "$(dirname "$0")/requirements.txt" > /dev/null 2>&1
python "$(dirname "$0")/run.py" "$@"
