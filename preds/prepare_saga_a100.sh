echo "Preparing saga. $@"
module purge   # Recommended for reproducibility
module --force swap StdEnv Zen2Env

bash ~/miniconda3/miniconda.sh -b -u -p $LOCALSCRATCH/miniconda3
source $LOCALSCRATCH/miniconda3/bin/activate

pip install -r requirements.txt
pip install litellm==1.67.6

