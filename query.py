import re, sys


### From: https://github.com/joelsare/web-tExplain/blob/main/tExplain-main/query.py


adjust = 1
query_line_num = []

with open(sys.argv[1]) as f:
    narrative = f.readlines()

queriesDir = sys.argv[2]
one_supp_regex = r"(\d) Where is (.*)\?"
two_supp_regex = r"(\d+) Where is the (.*)\?"
three_supp_regex = r"(\d+)? Where was the (.*) before the (.*)\?"
yes_no_regex = r"(\d+) Is (.*) in the (.*)\?"
counting_regex = r"(\d+) How many objects is (.*) carrying\?"
lists_regex = r"(\d+) What is (.*) carrying\?"

regexes = [(two_supp_regex,2),(three_supp_regex,3),(yes_no_regex,6),(counting_regex,7),(lists_regex,8)]

for line in narrative:
    for r in regexes:
        regex = r[0]
        val = r[1]
        match = None
        match = re.search(regex, line)
        if match:
            if val == 2: # two supporting facts
                qNum = int(match.group(1)) - adjust
                object = match.group(2)
                questions = ((qNum, object))
            elif val == 3: # three supporting facts
                object = match.group(2)
                loc2 = match.group(3)
                questions = ((object, loc2))
            elif val == 6: # yes no 
                lineNum = int(match.group(1)) - adjust
                person = match.group(2).lower()
                location = match.group(3).lower()
                questions = ((person, location, lineNum))
            elif val == 7: # counting
                lineNum = int(match.group(1)) - adjust
                person = match.group(2).lower()
                questions = ((person, lineNum))
            elif val == 8: # lists
                lineNum = int(match.group(1)) - adjust
                person = match.group(2).lower()
                questions = ((person, lineNum))
            filename = "query" + str(adjust) + ".txt"
            filename = queriesDir + '/' + filename
            query_line_num.append(int(match.group(1)))
            f = open(filename, "w")
            if val == 2:
                f.write('The %s is in the\n' % questions[1])
            # if val == 2: # two supporting facts
            #     f.write('%%!show_trace locationT2(%s,L,%d).\n' % (questions[1], questions[0]))
            # elif val == 3: # three supporting facts
            #     f.write('%%!show_trace lastChangeLoc(%s, L1, %s, T).\n' % (questions[0], questions[1]))
            # elif val == 6: # yes no 
            #     f.write('%%!show_trace notInLocation(%s, %s, B, %d).\n' % (questions[0], questions[1], questions[2]))
            #     f.write('%%!show_trace inLocation(%s, %s, B, %d).\n' % (questions[0], questions[1], questions[2]))
            #     f.write('is_aB(%s, %s).\n' % (questions[1], questions[1]))
            # elif val == 7: # counting
            #     f.write('%%!show_trace numberObjectsbyEntityatTime(N, %s, %d).\n' % (questions[0], questions[1]))
            # elif val == 8: # lists
            #     f.write('%%!show_trace entityCarrying(N, %s, %d).\n' % (questions[0], questions[1]))
            #     f.write('%%!show_trace entityNotCarrying(N, %s, %d).\n' % (questions[0], questions[1]))
            # for i in range(0,adjust):
            #     f.write('query(%s).\n' % (query_line_num[i]))
            f.close()

            adjust += 1
            break

# adjust = 1
# for q in questions:
#     filename = "query" + str(adjust) + ".lp"
#     filename = queriesDir + '/' + filename
#     f = open(filename, "w")
#     if val == 2: # two supporting facts
#         f.write('%%!show_trace locationT2(%s,L,%d).\n' % (q[1], q[0]))
#     elif val == 3: # three supporting facts
#         f.write('%%!show_trace changeLoc(%s, L1, %s, T).\n' % (q[0], q[1]))
#     elif val == 6: # yes no 
#         f.write('%%!show_trace notInLocation(%s, %s, %d).\n' % (q[0], q[1], q[2]))
#         f.write('%%!show_trace inLocation(%s, %s, %d).\n' % (q[0], q[1], q[2]))
#         f.write('is_aB(%s, %s).\n' % (q[1], q[1]))
#     elif val == 7: # counting
#         f.write('%%!show_trace numberObjectsbyEntityatTime(N, %s, %d).\n' % (q[0], q[1]))
#     elif val == 8: # lists
#         f.write('%%!show_trace entityCarrying(N, %s, %d).\n' % (q[0], q[1]))
#     adjust += 1
#     f.close()