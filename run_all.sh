#!/bin/bash

python3 optimize-prompts.py \
    --dataset dev_dwug_es.csv \
    --number-items 1 5 10 20 \
    --language-dataset es \
    --prompt-idiom en
