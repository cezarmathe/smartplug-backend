#!/bin/bash

OUTPUT="$(pwd)/output.txt"

cd src

echo "" > $OUTPUT

python3 app.py &> $OUTPUT
