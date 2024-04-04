import os

os.environ["HF_HOME"] = os.getcwd() + "/TransformerCACHE"

import transformers
from transformers import (
    AutoModelForCausalLM,
    pipeline,
    AutoTokenizer,
    AutoConfig,
    BitsAndBytesConfig,
)
import torch
import argparse
from torch.nn import DataParallel
from accelerate import infer_auto_device_map, init_empty_weights

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

model_id = args["model"]
model_name = pred = args["model"][args["model"].rfind("/") + 1 :].strip()

# Setting the device to cuda if there are GPU's available, CPU otherwise
device = "cuda" if torch.cuda.is_available() else "cpu"

# quantization_config = BitsAndBytesConfig(llm_int8_enable_fp32_cpu_offload=True)

tokenizer = AutoTokenizer.from_pretrained(
    model_id,
    return_tensors="pt",
    token=args["access_token"],
)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    device_map="auto",
    token=args["access_token"],
    # low_cpu_mem_usage=True,
)

# Wrap the model with DataParallel if there are multiple GPU's
if torch.cuda.device_count() > 1:
    model = DataParallel(model)


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

        inputs = tokenizer(prompt, return_tensors="pt")
        inputs["input_ids"] = inputs["input_ids"].to(device)

        # TODO: Test if setting to 2 tokens fixes compound words
        length = inputs["input_ids"].shape[1] + 2
        pred_full = tokenizer.decode(
            model.generate(
                inputs["input_ids"],
                max_length=length,
            )[0]
        )
        pred = pred_full[pred_full.rfind(" ") :].strip()

        preds.append((prompt, questions[i], pred, answers[i]))

        # TODO: handle discrepancies in capitalization
        if pred == answers[i]:
            accuracy += 1.0

        print(f"Prompt {i + 1}\n{prompt}")
        print(f"\nPrediction {i + 1}: {pred}")
        print(f"Answer {i + 1}: {answers[i]}\n")

    accuracy /= len(answers)

    print(f"Accuracy: {accuracy}")

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
