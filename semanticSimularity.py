# Prereq -> nltk.download('wordnet'), nltk.download('wordnet_ic'), nltk.download('omw-1.4')
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
import os
import pandas as pd

brown_ic = wordnet_ic.ic('ic-brown.dat')



'''
Path Similarity:
Return a score denoting how similar two word senses are,
based on the shortest path that connects the senses
in the is-a (hypernym/hypnoym) taxonomy.
The score is in the range 0 to 1.

wn.path_similarity(syns_1, syns_2)
'''

'''
Leacock-Chodorow Similarity:
Return a score denoting how similar two word senses are,
based on the shortest path that connects the senses (as above)
and the maximum depth of the taxonomy in which the senses occur.
The relationship is given as -log(p/2d)
where p is the shortest path length and d the taxonomy depth.

print(wn.lch_similarity(cat, dog))
'''

'''
Wu-Palmer Similarity:
Return a score denoting how similar two word senses are,
based on the depth of the two senses in the taxonomy
and that of their Least Common Subsumer (most specific ancestor node).

print(wn.wup_similarity(cat, dog))
'''


'''
Lin Similarity:
Return a score denoting how similar two word senses are,
based on the Information Content (IC) of the Least Common Subsumer
and that of the two input Synsets.
The relationship is given by the equation 2 * IC(lcs) / (IC(s1) + IC(s2)).

print(wn.lin_similarity(cat, dog, ic=brown_ic))
'''


'''
Resnik Similarity:
Return a score denoting how similar two word senses are,
based on the Information Content (IC) of the Least Common Subsumer
Note that for any similarity measure that uses information content,
the result is dependent on the corpus used to generate the information content
and the specifics of how the information content was created.

print(wn.res_similarity(cat, dog, ic=brown_ic))
'''


'''
Jiang-Conrath Similarity
Return a score denoting how similar two word senses are,
based on the Information Content (IC) of the Least Common Subsumer
and that of the two input Synsets.
The relationship is given by the equation 1 / (IC(s1) + IC(s2) - 2 * IC(lcs)).

print(wn.jcn_similarity(cat, dog, ic=brown_ic))
'''


# Example which should have no simularity: middle, garden
# Example which should have some simularity: yard, garden

# simularity = 0

# for syns_1 in wn.synsets('room'):
#     for syns_2 in wn.synsets('room'):
#         simularity = max(simularity, wn.wup_similarity(syns_1, syns_2))

# print(simularity)

os.chdir('predictions')
filelist = os.listdir()

dfs = []
df_names = []
averages = []

for file in filelist:
    dfs.append(pd.read_csv(file))
    df_names.append(file)
    # df = pd.read_csv(file)

for df in dfs:
    predictions = df['Prediction']
    answers = df['Answer']
    simularities = []

    for i in range(len(predictions)):
        simularity = 0
        # if not predictions[i].isnull():

        for syns_1 in wn.synsets(predictions[i]):
            for syns_2 in wn.synsets(answers[i]):
                simularity = max(simularity, wn.wup_similarity(syns_1, syns_2))
        simularities.append(simularity)

    averages.append(sum(simularities) / len(simularities))
    df["Simularity"] = simularities
    print(df, end='\n\n')

for i in range(len(df_names)):
    print(f"Average simularity score of {df_names[i]}: {averages[i]}")


