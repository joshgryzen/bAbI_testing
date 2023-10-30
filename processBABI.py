import os
import glob
import configparser
import re
import shutil
from sys import argv


# Code modified from https://github.com/joelsare/web-tExplain/blob/main/tExplain-main/runbAbI.py

# 1 – Single Supporting Facts
# 2 – Two Supporting Facts
# 3 – Three Supporting Facts
# 5 – Three Argument Relations
# 6 – Yes/No Questions
# 7 – Counting
# 8 – Lists/Sets


def process():
    i = 0
    current = 0
    narrativeName = "Narrative" + str(current + 1) + ".txt"
    narrativeFile = open(narrativeName, "w")
    questionName = "Question" + str(current + 1) + ".txt"
    questionFile = open(questionName, "w")
    seen = 0
    while i < len(narrative):
        line = narrative[i]
        i += 1
        if "?" in line:
            current += 1
            if seen < current:
                question = processQuestion(line)
                print(question[0], file=questionFile)
                print(question[1], file=questionFile, end="")
                seen += 1
                if i == len(narrative) - 1:
                    break
                narrativeFile.close()
                questionFile.close()
                narrativeName = "Narrative" + str(current + 1) + ".txt"
                narrativeFile = open(narrativeName, "w")
                questionName = "Question" + str(current + 1) + ".txt"
                questionFile = open(questionName, "w")
                i = 0
                current = 0
        else:
            print(re.sub("^\d+ ", "", line), file=narrativeFile, end="")

def processQuestion(question):
    # question = re.sub("^\d+ ", "", question)
    questionAnswer = question.split('?')
    questionAnswer[0] += '?'
    questionAnswer[1] = questionAnswer[1].strip().split('\t')[0]
    

    adjust = 1

    one_supp_regex = r"(\d) Where is (.*)\?"
    two_supp_regex = r"(\d+) Where is the (.*)\?"
    three_supp_regex = r"(\d+)? Where was the (.*) before the (.*)\?"
    yes_no_regex = r"(\d+) Is (.*) in the (.*)\?"
    counting_regex = r"(\d+) How many objects is (.*) carrying\?"
    lists_regex = r"(\d+) What is (.*) carrying\?"

    regexes = [(one_supp_regex,1), (two_supp_regex,2)] # ,(three_supp_regex,3),(yes_no_regex,6),(counting_regex,7),(lists_regex,8)

    for r in regexes:
        regex = r[0]
        val = r[1]
        match = None
        match = re.search(regex, questionAnswer[0])
        if match:
            if val == 1:
                qNum = int(match.group(1)) - adjust
                object = match.group(2)
                questions = ((qNum, object))
            elif val == 2: # two supporting facts
                qNum = int(match.group(1)) - adjust
                object = match.group(2)
                questions = ((qNum, object))
            # elif val == 3: # three supporting facts
            #     object = match.group(2)
            #     loc2 = match.group(3)
            #     questions = ((object, loc2))
            # elif val == 6: # yes no 
            #     lineNum = int(match.group(1)) - adjust
            #     person = match.group(2).lower()
            #     location = match.group(3).lower()
            #     questions = ((person, location, lineNum))
            # elif val == 7: # counting
            #     lineNum = int(match.group(1)) - adjust
            #     person = match.group(2).lower()
            #     questions = ((person, lineNum))
            # elif val == 8: # lists
            #     lineNum = int(match.group(1)) - adjust
            #     person = match.group(2).lower()
            #     questions = ((person, lineNum))
            if val == 1:
                questionAnswer[0] = ('%s is in the' % questions[1])
            elif val == 2:
                questionAnswer[0] = ('The %s is located in the' % questions[1])
            adjust += 1
            break

    return questionAnswer
    
filename = os.path.basename(argv[1]).replace(".txt", "")

with open(argv[1]) as f:
    narrative = f.readlines()

# GENERATE NARRATIVES
if os.path.exists(filename):
    shutil.rmtree(filename)
os.mkdir(filename)
os.chdir(filename)
process()

# GENERATE QUERIES

# os.chdir('..')
# if not os.path.exists("query_1"):
#     os.mkdir("query_1")
# command = "python query.py %s %s" % (argv[1], "\query_1")
# os.system(command)
