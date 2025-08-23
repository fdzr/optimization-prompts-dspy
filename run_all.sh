#!/bin/bash

python3 optimize-prompts.py \
    --train-data train_es.csv \
    --dev-data dev_es.csv \
    --number-items-dev-set 50 \
    --number-items 20 \
    --language-dataset es \
    --prompt-idiom es
