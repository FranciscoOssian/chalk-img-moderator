#!/bin/bash

lsof -i :8000 | awk 'NR>1 {print $2}' | xargs kill

#export PYTHON_SERVER_KEY=value
gunicorn main:app