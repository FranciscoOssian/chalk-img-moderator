#!/bin/bash

lsof -i :8000 | awk 'NR>1 {print $2}' | xargs kill

gunicorn main:app