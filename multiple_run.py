import os

# Bloom tests

# No Context
os.system('python predict.py --m=bigscience/bloomz-560m --t=qa1_single-supporting-fact_train.txt')
os.system('python predict.py --m=bigscience/bloomz-1b1 --t=qa1_single-supporting-fact_train.txt')
os.system('python predict.py --m=bigscience/bloomz-3b --t=qa1_single-supporting-fact_train.txt')
# With Context
os.system('python predict.py --m=bigscience/bloomz-560m --t=qa1_single-supporting-fact_train.txt --context')
os.system('python predict.py --m=bigscience/bloomz-1b1 --t=qa1_single-supporting-fact_train.txt --context')
os.system('python predict.py --m=bigscience/bloomz-3b --t=qa1_single-supporting-fact_train.txt --context')

# OPT tests

# No Context
os.system('python predict.py --m=facebook/opt-350m --t=qa1_single-supporting-fact_train.txt')
os.system('python predict.py --m=facebook/opt-1.3b --t=qa1_single-supporting-fact_train.txt')
os.system('python predict.py --m=facebook/opt-2.7b --t=qa1_single-supporting-fact_train.txt')

# With Context
os.system('python predict.py --m=facebook/opt-350m --t=qa1_single-supporting-fact_train.txt --context')
os.system('python predict.py --m=facebook/opt-1.3b --t=qa1_single-supporting-fact_train.txt --context')
os.system('python predict.py --m=facebook/opt-2.7b --t=qa1_single-supporting-fact_train.txt --context')





