#!/bin/bash

wrapperfunction() {
    source prepare_saga_a100.sh
}
wrapperfunction


cd ~/nn9851k/nikolare/llms/bin

# find the first vacant port 
OPORT=11434
while netstat -tlnp | grep -q ":$OPORT "; do
	  ((OPORT++))
done

echo "Starting ollama on $(hostname):$OPORT"
OLLAMA_MODELS=../models/ OLLAMA_HOST=0.0.0.0:$OPORT ./ollama serve &>ollama_$(hostname)_${OPORT}.log &
cd -

DSPY_CACHEDIR=".dspy_cache_$(hostname)_${OPORT}" NO_PROXY=localhost,127.0.0.1 python annotate_sp.py $OPORT $@
