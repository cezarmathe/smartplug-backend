#!/bin/bash

cd src

python3 app.py

mv "logs/latest.log" "logs/$(date)"
