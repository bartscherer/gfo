#!/bin/sh
if [ -e /app/prestart.py ]
then
    python3 /app/prestart.py
else
    SCRIPT=$(readlink -f "$0")
    SCRIPTPATH=$(dirname "$SCRIPT")
    python3 "${SCRIPTPATH}/prestart.py"
fi
