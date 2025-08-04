#!/bin/bash

python3 optimization-for-dwug-es-prompt-es.py &
python3 optimization-for-dwug-es-prompt-en.py &
python3 optimization-for-dwug-en-prompt-en.py &
python3 optimization-for-dwug-en-prompt-es.py &

wait