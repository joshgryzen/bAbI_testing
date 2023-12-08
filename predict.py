import transformers
from transformers import BloomForCausalLM, BloomTokenizerFast, pipeline
import torch
import argparse
import os
import csv

from processBABI import *

# command line args, narrative text file name, size of model -> defaults to 560m
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model', required=True, type=str, help="Link to Hugging Face Model, i.e.: bigscience/bloom-560m")
parser.add_argument('-t', '--task', required=True, type=str, help="The name of the txt file to be processed, i.e.: qa1_single-supporting-fact_train.txt")
parser.add_argument('-n', '--nsize', default=100, type=int, help="The maximum size of the narrative. Default set to 100")
parser.add_argument('-c', '--context', nargs='?', const=True, default=False, type=bool, help="Option to pass in additional context before each narrative. Default set to false")

args = vars(parser.parse_args())
print(args)
# Process BABI file
filename = os.path.basename(args["task"]).replace(".txt", "")

process(args["task"], args['nsize'], args['context'])
generator = pipeline('text-generation', model=args['model'], max_new_tokens=1)

# model = BloomForCausalLM.from_pretrained(args['model'])
# tokenizer = BloomTokenizerFast.from_pretrained(args['model'])

# Example usage with Beam Search
'''

prompt = "It was a dark and stormy night"
result_length = 50
inputs = tokenizer(prompt, return_tensors="pt")

# Beam Search
print(tokenizer.decode(model.generate(inputs["input_ids"], max_length = result_length, num_beams = 2, no_repeat_ngram_size = 2, early_stopping = True)[0]))

'''

### ------------------------- Task 2 First 10 Narratives ------------------------- ###
#region Narratives by hand

# Task 2 First 10 narratives
narrative_1 = "Mary moved to the bathroom. Sandra journeyed to the bedroom. Mary got the football there. John went to the kitchen. Mary went back to the kitchen. Mary went back to the garden." # Where is the football? 	garden	3 6
narrative_2 = "Sandra went back to the office. John moved to the office. Sandra journeyed to the hallway. Daniel went back to the kitchen. Mary dropped the football. John got the milk there." # Where is the football? 	garden	12 6
narrative_3 = "Mary took the football there. Sandra picked up the apple there. Mary travelled to the hallway. John journeyed to the kitchen." # Where is the football? 	hallway	15 17"
narrative_4 = "John moved to the hallway. Sandra left the apple." # Where is the apple? 	hallway	21 10"
narrative_5 = "Mary got the apple there. John travelled to the garden. John went back to the hallway. John went back to the bedroom. Mary journeyed to the bedroom. John journeyed to the kitchen. John left the milk. Mary left the apple." # Where is the milk? 	kitchen	29 28"
narrative_6 = "Daniel went to the kitchen. Daniel journeyed to the hallway. Mary went back to the garden. Daniel picked up the apple there. Sandra went to the office. Sandra travelled to the bedroom. Mary got the football there. Sandra grabbed the milk there. Mary left the football. Daniel left the apple." # Where is the football? 	garden	9 3"
narrative_7 = "Daniel got the apple there. Sandra dropped the milk." # Where is the milk? 	bedroom	13 6"
narrative_8 = "Mary picked up the football there. John moved to the bathroom." # Where is the milk? 	bedroom	13 6"
narrative_9 = "Mary moved to the bedroom. Sandra went to the garden." # Where is the milk? 	bedroom	13 6"
narrative_10 = "Daniel discarded the apple. Daniel went to the bathroom." # Where is the apple? 	hallway	21 2"

question_1 = "The football is in the" # A: garden 3 6
question_2 = "The football is in the" # A: garden 12 6
question_3 = "The football is in the" # A: hallway 15 17
question_4 = "The apple is in the" # A: hallway 21 10
question_5 = "The milk is in the" # A: kitchen 29 28
question_6 = "The football is in the" # A: garden 9 3
question_7 = "The milk is in the" # A: bedroom 13 6
question_8 = "The milk is in the" # A: bedroom 13 6
question_9 = "The milk is in the" # A: bedroom 13 6
question_10 = "The apple is in the" # hallway 21 2

### ------------------------- Combined Narrative ------------------------- ###
def predictCombined(): 

    combined_narrative = narrative_1 + " " + narrative_2 + " " + narrative_3 + " " + narrative_4 + " " + narrative_5 + " " + narrative_6 + " " + narrative_7 + " " + narrative_8 + " " + narrative_9  + " " + narrative_10

    ### Question 1 - 3

    prompt_1 = combined_narrative + " " + question_1
    inputs_1 = tokenizer(prompt_1, return_tensors="pt")

    length_1 = (inputs_1["input_ids"].shape[1] + 1)

    pred_1 = tokenizer.decode(model.generate(inputs_1["input_ids"], max_length = length_1, num_beams = 2, no_repeat_ngram_size = 2, early_stopping = True)[0])

    print(f"Prompt 1\n{prompt_1}")
    print(f"\nPrediction 1: {pred_1[pred_1.rfind(' '): ]}\n")

    ### Question 4

    prompt_4 = combined_narrative + " " + question_4
    inputs_4 = tokenizer(prompt_4, return_tensors="pt")

    length_4 = (inputs_4["input_ids"].shape[1] + 1)

    pred_4 = tokenizer.decode(model.generate(inputs_4["input_ids"], max_length = length_4, num_beams = 2, no_repeat_ngram_size = 2, early_stopping = True)[0])

    print(f"Prompt 4\n{prompt_4}")
    print(f"\nPrediction 4: {pred_4[pred_4.rfind(' '): ]}\n")

    ### Question 5

    prompt_5 = combined_narrative + " " + question_5
    inputs_5 = tokenizer(prompt_5, return_tensors="pt")

    length_5 = (inputs_5["input_ids"].shape[1] + 1)

    pred_5 = tokenizer.decode(model.generate(inputs_5["input_ids"], max_length = length_5, num_beams = 2, no_repeat_ngram_size = 2, early_stopping = True)[0])

    print(f"Prompt 5\n{prompt_5}")
    print(f"\nPrediction 5: {pred_5[pred_5.rfind(' '): ]}\n")

### ------------------------- Progressive Narrative ------------------------- ###
def predictProgressive():

    narratives = []
    questions = []
    answers = []

    for files in os.listdir():
        print(files)

    # narratives = [narrative_1, narrative_2, narrative_3, narrative_4, narrative_5, narrative_6, narrative_7, narrative_8, narrative_9, narrative_10]
    # questions = [question_1, question_2, question_3, question_4, question_5, question_6, question_7, question_8, question_9, question_10]

    for i in range(0, 10):
        prompt = ""
        question = questions[i]

        for j in range(0, i + 1):
            prompt += narratives[j] + " "

        prompt += question
        inputs = tokenizer(prompt, return_tensors="pt")

        length = (inputs["input_ids"].shape[1] + 1)

        pred = tokenizer.decode(model.generate(inputs["input_ids"], max_length = length, num_beams = 2, no_repeat_ngram_size = 2, early_stopping = True)[0])

        print(f"Prompt {i + 1}\n{prompt}")
        print(f"\nPrediction {i + 1}: {pred[pred.rfind(' '): ]}\n")


#endregion


def predict():
    narratives = []
    questions = []
    answers = []
    preds = []

    accuracy = 0.0

    filelist = os.listdir()

    for i in range(1, len(filelist) // 2 + 1):

        # Append narratives
        with open('Narrative%s.txt' % str(i)) as f:
            narratives.append(''.join(f.readlines()).replace('\n', ' '))
        f.close()
        
        # Append questions and answers
        with open('Question%s.txt' % str(i)) as f:
            questions.append(''.join(f.readlines(1)).replace('\n', ''))
            answers.append(''.join(f.readlines(2)).replace('\n', ''))
        f.close()

    os.chdir('..')
    os.chdir('predictions')

    # predfile = open(f"{filename}_{size}_Preds.txt", "w")

    for i in range(0, len(narratives)):
        # context = "The following is a story with characters moving to different locations. Assume the most recent location is the character's current location. "
        if(args['task'] == 'qa1_single-supporting-fact_train.txt'):
            context = "The following is a narrative with characters moving to different locations. Assume the character's most recent reference refers to their current location. "
        elif(args['task'] == 'qa2_two-supporting-facts_train.txt'):
            context = "The following is a narrative with characters moving to different locations. The characters can pick up objects and bring the objects to new locations. Assume the object's most recent reference refers to their current location. "
        prompt = context + narratives[i] if args['context'] else narratives[i]
        question = questions[i]

        prompt += question
        # inputs = tokenizer(prompt, return_tensors="pt")

        # length = (inputs["input_ids"].shape[1] + 1)
        

        # pred_full = tokenizer.decode(model.generate(inputs["input_ids"], max_length = length, num_beams = 2, no_repeat_ngram_size = 2, early_stopping = True)[0])
        # pred_full = tokenizer.decode(model.generate(inputs["input_ids"], max_length = length)[0])
        # pred = pred_full[pred_full.rfind(' '): ].strip()

        # generator = pipeline('text-generation', model=args['model'], max_new_tokens=1)

        
        pred_full = generator(prompt)[0]['generated_text']
        pred = pred_full[pred_full.rfind(' '): ].strip()


        # pred = pred_full[pred_full.rfind(' '): ].strip()
        
        preds.append((prompt, questions[i], pred, answers[i]))

        if pred == answers[i]: accuracy += 1.0

        # print(f"Prompt {i + 1}\n{prompt}", file=predfile)
        # print(f"\nPrediction {i + 1}: {pred}", file=predfile)
        # print(f"Answer {i + 1}: {answers[i]}\n", file=predfile)
        
        print(f"Prompt {i + 1}\n{prompt}")
        print(f"\nPrediction {i + 1}: {pred}")
        # print(f"Generator prediction {i + 1}: {pred}")
        print(f"Answer {i + 1}: {answers[i]}\n")

    accuracy /= len(answers)

    # print(f"Accuracy: {accuracy}", file=predfile)
    print(f"Accuracy: {accuracy}")

    print(os.listdir())

    model_name = pred = args['model'][args['model'].rfind('/') + 1: ].strip()

    fname = f"WITH_CONTEXT_{model_name}_{filename}_Preds.csv" if args['context'] else f"{model_name}_{filename}_Preds.csv"

    with open(fname,"w") as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['Prompt', 'Cloze', 'Prediction', 'Answer'])
        csv_out.writerows(preds)
        csv_out.writerow(['Accuracy: ', {accuracy}])

predict()