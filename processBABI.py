import os
import glob
import configparser
import re
import shutil
from sys import argv

# 1 – Single Supporting Facts
# 2 – Two Supporting Facts
# 3 – Three Supporting Facts
# 5 – Three Argument Relations
# 6 – Yes/No Questions
# 7 – Counting
# 8 – Lists/Sets


def process(name):
    i = 0
    current = 0
    narrativeName = name + "Narrative" + str(current + 1) + ".txt"
    narrativeFile = open(narrativeName, "w")
    questionName = name + "Question" + str(current + 1) + ".txt"
    questionFile = open(questionName, "w")
    seen = 0
    while i < len(narrative):
        line = narrative[i]
        i += 1
        if "?" in line:
            current += 1
            if seen < current:
                print(re.sub("^\d+ ", "", line), file=questionFile, end="")
                seen += 1
                if i == len(narrative):
                    break
                narrativeFile.close()
                questionFile.close()
                narrativeName = name + "Narrative" + str(current + 1) + ".txt"
                narrativeFile = open(narrativeName, "w")
                questionName = name + "Question" + str(current + 1) + ".txt"
                questionFile = open(questionName, "w")
                i = 0
                current = 0
        else:
            print(re.sub("^\d+ ", "", line), file=narrativeFile, end="")


filename = os.path.basename(argv[1]).replace(".txt", "")

with open(argv[1]) as f:
    narrative = f.readlines()

config = configparser.ConfigParser()
config.read("config.ini")
tuplesDir = config["APP"]["tuples_directory"]
queriesDir = config["APP"]["queries_directory"]
baseDir = os.getcwd()


# GENERATE NARRATIVES
os.chdir(tuplesDir)
if os.path.exists(filename):
    shutil.rmtree(filename)
os.mkdir(filename)
os.chdir(filename)
specificTupleDir = os.getcwd()
process(filename)

# GENERATE QUERIES
command = "python query.py %s %s" % (argv[1], queriesDir)
os.system(command)
