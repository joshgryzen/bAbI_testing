# bAbI_testing
 
Run predict.py to test a hugging face model on the BABI dataset. 

optional parameters: 
    --nsize (int) for the size of the narrative
    --context (bool) can add context to the narrative

bloom models: 560m, 1b1, 1b7, 3b, 7b1, 176b
bloom example: 

`python predict.py --model=bigscience/bloom-560m --task=qa1_single-supporting-fact_train.txt`

opt models: 125m, 350m, 1.3b, 2.7b, 6.7b, 13b, 30b, 66b, 175b
opt example: 

`python predict.py --model=facebook/opt-1.3b --task=qa1_single-supporting-fact_train.txt`
