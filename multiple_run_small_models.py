import os

# region Bloomz tests

# Single Supporting Fact

# No Context
os.system('python predict.py --m=bigscience/bloomz-560m --t=qa1_single-supporting-fact_train.txt')
os.system('python predict.py --m=bigscience/bloomz-1b1 --t=qa1_single-supporting-fact_train.txt')
os.system('python predict.py --m=bigscience/bloomz-3b --t=qa1_single-supporting-fact_train.txt')
# With Context
os.system('python predict.py --m=bigscience/bloomz-560m --t=qa1_single-supporting-fact_train.txt --context')
os.system('python predict.py --m=bigscience/bloomz-1b1 --t=qa1_single-supporting-fact_train.txt --context')
os.system('python predict.py --m=bigscience/bloomz-3b --t=qa1_single-supporting-fact_train.txt --context')

# Two Supporting Facts 

# No Context
os.system('python predict.py --m=bigscience/bloomz-560m --t=qa2_two-supporting-facts_train.txt')
os.system('python predict.py --m=bigscience/bloomz-1b1 --t=qa2_two-supporting-facts_train.txt')
os.system('python predict.py --m=bigscience/bloomz-3b --t=qa2_two-supporting-facts_train.txt')
# With Context
os.system('python predict.py --m=bigscience/bloomz-560m --t=qa2_two-supporting-facts_train.txt --context')
os.system('python predict.py --m=bigscience/bloomz-1b1 --t=qa2_two-supporting-facts_train.txt --context')
os.system('python predict.py --m=bigscience/bloomz-3b --t=qa2_two-supporting-facts_train.txt --context')

# endregion

# region Bloom tests

# Single Supporting Fact

# No Context
os.system('python predict.py --m=bigscience/bloom-560m --t=qa1_single-supporting-fact_train.txt')
os.system('python predict.py --m=bigscience/bloom-1b1 --t=qa1_single-supporting-fact_train.txt')
os.system('python predict.py --m=bigscience/bloom-3b --t=qa1_single-supporting-fact_train.txt')
# With Context
os.system('python predict.py --m=bigscience/bloom-560m --t=qa1_single-supporting-fact_train.txt --context')
os.system('python predict.py --m=bigscience/bloom-1b1 --t=qa1_single-supporting-fact_train.txt --context')
os.system('python predict.py --m=bigscience/bloom-3b --t=qa1_single-supporting-fact_train.txt --context')

# Two Supporting Facts 

# No Context
os.system('python predict.py --m=bigscience/bloom-560m --t=qa2_two-supporting-facts_train.txt')
os.system('python predict.py --m=bigscience/bloom-1b1 --t=qa2_two-supporting-facts_train.txt')
os.system('python predict.py --m=bigscience/bloom-3b --t=qa2_two-supporting-facts_train.txt')
# With Context
os.system('python predict.py --m=bigscience/bloom-560m --t=qa2_two-supporting-facts_train.txt --context')
os.system('python predict.py --m=bigscience/bloom-1b1 --t=qa2_two-supporting-facts_train.txt --context')
os.system('python predict.py --m=bigscience/bloom-3b --t=qa2_two-supporting-facts_train.txt --context')

# endregion

# region OPT tests

# Single Supporting Fact

# No Context
os.system('python predict.py --m=facebook/opt-350m --t=qa1_single-supporting-fact_train.txt')
os.system('python predict.py --m=facebook/opt-1.3b --t=qa1_single-supporting-fact_train.txt')
os.system('python predict.py --m=facebook/opt-2.7b --t=qa1_single-supporting-fact_train.txt')
# With Context
os.system('python predict.py --m=facebook/opt-350m --t=qa1_single-supporting-fact_train.txt --context')
os.system('python predict.py --m=facebook/opt-1.3b --t=qa1_single-supporting-fact_train.txt --context')
os.system('python predict.py --m=facebook/opt-2.7b --t=qa1_single-supporting-fact_train.txt --context')

# Two Supporting Facts 

# No Context
os.system('python predict.py --m=facebook/opt-350m --t=qa2_two-supporting-facts_train.txt.txt')
os.system('python predict.py --m=facebook/opt-1.3b --t=qa2_two-supporting-facts_train.txt.txt')
os.system('python predict.py --m=facebook/opt-2.7b --t=qa2_two-supporting-facts_train.txt.txt')
# With Context
os.system('python predict.py --m=facebook/opt-350m --t=qa2_two-supporting-facts_train.txt.txt --context')
os.system('python predict.py --m=facebook/opt-1.3b --t=qa2_two-supporting-facts_train.txt.txt --context')
os.system('python predict.py --m=facebook/opt-2.7b --t=qa2_two-supporting-facts_train.txt.txt --context')


# endregion





