import json
import os

os.environ["HF_HOME"] = os.getcwd() + "/TransformerCACHE"

import argparse
from huggingface_hub import InferenceClient
from tenacity import retry, stop_after_attempt, wait_fixed

from handle_http_429_errors import (
    retry_if_http_429_error,
    wait_for_retry_after_header
)

import csv

from processBABI import *

@retry(
    retry=retry_if_http_429_error(),
    wait=wait_for_retry_after_header(fallback=wait_fixed(1))
)

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
    default=1000,
    type=int,
    help="The maximum size of the narrative. Default set to 1000",
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
parser.add_argument(
    "-at",
    "--access_token",
    nargs="?",
    default="",
    type=str,
    help="Hugging face access token",
)

args = vars(parser.parse_args())
# Process BABI file
filename = os.path.basename(args["task"]).replace(".txt", "")


process(args["task"], args["nsize"], args["context"])

# The full 176 billion parameter bloom model!
model = args["model"]
# model = "meta-llama/Llama-2-70b-hf"
inference = InferenceClient(model, token="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")

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
        if (
            args["task"] == "qa1_single-supporting-fact_train.txt"
            or args["task"] == "qa1_single-supporting-fact_test.txt"
        ):
            context = "The following is a narrative with characters moving to different locations. Assume the character's most recent reference refers to their current location. "
        elif (
            args["task"] == "qa2_two-supporting-facts_train.txt"
            or args["task"] == "qa3_three-supporting-facts_train.txt"
            or args["task"] == "qa2_two-supporting-facts_test.txt"
            or args["task"] == "qa3_three-supporting-facts_test.txt"
        ):
            context = "The following is a narrative with characters moving to different locations. The characters can pick up objects and bring the objects to new locations. Assume the object's most recent reference refers to their current location. "
        prompt = context + narratives[i] if args["context"] else narratives[i]
        question = questions[i]

        prompt += question

        # TODO: handle rate limit reached and save checkpoint
        try: 
            pred = inference.text_generation(prompt, model=model, max_new_tokens=2).strip().replace(".", "")

        # # load the json and get the string result
        # pred_full = json.loads(pred_result)[0]["generated_text"]

        # pred = pred_full[pred_full.rfind(" ") :].strip().replace(".", "")

        preds.append((prompt, questions[i], pred, answers[i]))

        if pred == answers[i]:
            accuracy += 1.0

        print(f"Prompt {i + 1}\n{prompt}")
        print(f"\nPrediction {i + 1}: {pred}")
        print(f"Answer {i + 1}: {answers[i]}\n")

    accuracy /= len(answers)

    print(f"Accuracy: {accuracy}")

    if not os.path.exists(model):
        os.mkdir(model)

    os.chdir(model)

    fname = (
        f"WITH_CONTEXT_{model}_{filename}_Preds.csv"
        if args["context"]
        else f"{model}_{filename}_Preds.csv"
    )

    with open(fname, "w") as out:
        csv_out = csv.writer(out)
        csv_out.writerow(["Prompt", "Cloze", "Prediction", "Answer"])
        csv_out.writerows(preds)
        csv_out.writerow(["Accuracy: ", {accuracy}])


predict()
