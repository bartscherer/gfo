#!/usr/bin/env bash

PROD=true;

while getopts "p:" arg; do
  case $arg in
    p) PROD=$OPTARG;;
  esac
done

# Turn on bash's job control
set -m

# Execute pre-start script
chmod +x prestart.sh
./prestart.sh

# Start the server process and put it in the background
if [ "$PROD" == "false" ]; then
    echo "RUNNING IN DEBUG MODE"
    gunicorn main:app --workers 4 --worker-class main.GFOUvicornWorker --bind 0.0.0.0:3000 --reload --log-level debug &
else
    gunicorn main:app --workers 4 --worker-class main.GFOUvicornWorker --bind 0.0.0.0:80 &
fi

# Start the service manager
python3 servicemanager.py

# Bring server process to foreground
fg %1