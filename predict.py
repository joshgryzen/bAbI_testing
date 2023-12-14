import transformers
from transformers import AutoModelForCausalLM, pipeline, AutoTokenizer
import torch
import argparse
import os
import csv

from processBABI import *

# command line args, narrative text file name, size of model -> defaults to 560m
parser = argparse.ArgumentParser()
parser.add_argument(
    "-m",
    "--model",
    required=True,
    type=str,
    help="Link to Hugging Face Model, i.e.: bigscience/bloom-560m",
)
parser.add_argument(
    "-t",
    "--task",
    required=True,
    type=str,
    help="The name of the txt file to be processed, i.e.: qa1_single-supporting-fact_train.txt",
)
parser.add_argument(
    "-n",
    "--nsize",
    default=100,
    type=int,
    help="The maximum size of the narrative. Default set to 100",
)
parser.add_argument(
    "-c",
    "--context",
    nargs="?",
    const=True,
    default=False,
    type=bool,
    help="Option to pass in additional context before each narrative. Default set to false",
)

args = vars(parser.parse_args())
# Process BABI file
filename = os.path.basename(args["task"]).replace(".txt", "")


process(args["task"], args["nsize"], args["context"])

model_id = args["model"]
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)

# if args["model"] == "bigscience/bloom":
#     generator = pipeline(
#         "text-generation", model=args["model"], max_new_tokens=1, from_pt=True
#     )
# else:
#     generator = pipeline("text-generation", model=args["model"], max_new_tokens=1)

# model = BloomForCausalLM.from_pretrained(args['model'])
# tokenizer = BloomTokenizerFast.from_pretrained(args['model'])

# Example usage with Beam Search
"""

prompt = "It was a dark and stormy night"
result_length = 50
inputs = tokenizer(prompt, return_tensors="pt")

# Beam Search
print(tokenizer.decode(model.generate(inputs["input_ids"], max_length = result_length, num_beams = 2, no_repeat_ngram_size = 2, early_stopping = True)[0]))

"""


def predict():
    narratives = []
    questions = []
    answers = []
    preds = []

    accuracy = 0.0

    filelist = os.listdir()

    for i in range(1, len(filelist) // 2 + 1):
        # Append narratives
        with open("Narrative%s.txt" % str(i)) as f:
            narratives.append("".join(f.readlines()).replace("\n", " "))
        f.close()

        # Append questions and answers
        with open("Question%s.txt" % str(i)) as f:
            questions.append("".join(f.readlines(1)).replace("\n", ""))
            answers.append("".join(f.readlines(2)).replace("\n", ""))
        f.close()

    os.chdir("..")
    os.chdir("predictions")

    for i in range(0, len(narratives)):
        if args["task"] == "qa1_single-supporting-fact_train.txt":
            context = "The following is a narrative with characters moving to different locations. Assume the character's most recent reference refers to their current location. "
        elif args["task"] == "qa2_two-supporting-facts_train.txt":
            context = "The following is a narrative with characters moving to different locations. The characters can pick up objects and bring the objects to new locations. Assume the object's most recent reference refers to their current location. "
        prompt = context + narratives[i] if args["context"] else narratives[i]
        question = questions[i]

        prompt += question

        inputs = tokenizer(prompt, return_tensors="pt")
        pred_full = tokenizer.decode(
            model.generate(
                inputs["input_ids"],
                max_length=len(inputs["input_ids"]) + 1,
            )[0]
        )

        # pred_full = generator(prompt)[0]["generated_text"]
        pred = pred_full[pred_full.rfind(" ") :].strip()

        preds.append((prompt, questions[i], pred, answers[i]))

        if pred == answers[i]:
            accuracy += 1.0

        print(f"Prompt {i + 1}\n{prompt}")
        print(f"\nPrediction {i + 1}: {pred}")
        print(f"Answer {i + 1}: {answers[i]}\n")

    accuracy /= len(answers)

    print(f"Accuracy: {accuracy}")

    model_name = pred = args["model"][args["model"].rfind("/") + 1 :].strip()

    if not os.path.exists(model_name):
        os.mkdir(model_name)

    os.chdir(model_name)

    fname = (
        f"WITH_CONTEXT_{model_name}_{filename}_Preds.csv"
        if args["context"]
        else f"{model_name}_{filename}_Preds.csv"
    )

    with open(fname, "w") as out:
        csv_out = csv.writer(out)
        csv_out.writerow(["Prompt", "Cloze", "Prediction", "Answer"])
        csv_out.writerows(preds)
        csv_out.writerow(["Accuracy: ", {accuracy}])


predict()
