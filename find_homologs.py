# python find_homologs.py [database] [family] [scoring matrix]
#
# Implementation of a profile-based algorithm to find novel (higher than 3 
# standard deviations) homologs of a family of sequences in a database
# using scoring matrix.
# Outputs each novel homolog, its score, and its corresponding p-value

import numpy as np
import sys

def loadData(db_file, fam_file, sm_file):
    db = [line.rstrip('\r\n') for line in open(db_file)][0]
    F = [line.rstrip('\r\n') for line in open(fam_file)]
    matrix = [line.rstrip('\r\n') for line in open(sm_file)]

    residue_dict = list()
    residues = matrix[0].split()

    for i in range(0, len(residues)):
        residue_dict.append(residues[i])

    mat = []

    for i in range(1, len(matrix)-1):
        line = matrix[i].split()
        line = line[1:] # cut off the residue label

        diff = len(residues) - len(line)
        if diff != 0:
            for j in range(diff):
                line.insert(0, 0)

        mat.append(line)

    for i in range(1, len(mat)):
        for j in range(0, i+1):
            mat[i][j] = int(mat[j][i])

    return db, F1, mat, residue_dict    

def buildScore(family, t_matrix, residue_dict):
    seq_length = family[0]
    family_size = len(family)
    # initialize freq matrix -- residue dictionary x seq length
    freq = []
    for i in range(len(residue_dict)):
        row = [0] * len(seq_length)
        freq.append(row)

    # loop through each seq in family to fill freq matrix
    for i in range(family_size):
        for j in range(len(family[i])):
            letter = family[i][j]

            freq[residue_dict.index(letter)][j] += 1

    # divide the counts by the number of sequences in the family to get final frequency matrix
    for row in range(len(freq)):
        for col in range(len(freq[0])):
            if freq[row][col] != 0:
                freq[row][col] = float(freq[row][col]) / family_size

    # initialize score matrix
    score = []
    for i in range(len(residue_dict)):
        row = [0] * len(family[0])
        score.append(row)

    freq_T = zip(*freq)

    # fill score matrix
    for i in range(len(residue_dict)):
        for j in range(len(family[0])):
            entry = 0

            for col in range(len(freq_T[0])):
                if freq_T[j][col] != 0:
                    entry += freq_T[j][col] * int(t_matrix[i][col])

            score[i][j] = entry

    return score

def getScores(db, score, residue_dict):
    score_list = []

    kmer_len = len(score[0])

    # i keeps track of starting position in db
    for i in range(len(db) - kmer_len + 1):
        kmer = db[i:i+kmer_len]
        s = 0   # score of kmer

        # j iterates through kmer starting at i
        for j in range(0, kmer_len):
            letter = db[i+j]
            s += score[residue_dict.index(letter)][j]

        score_list.append((kmer, s))

    return score_list   # score_dict

def findHomologs(db, family, transition_matrix, residue_dict):
    # specify which family to build score matrix for
    score = buildScore(family, transition_matrix, residue_dict)

    # set threshold by shuffling db and getting scores
    l = list(db)
    random.shuffle(l)
    rand_db = ''.join(l)

    rand_scores = getScores(rand_db, score, residue_dict)
    rand_s_list = [x[1] for x in rand_scores]
    threshold = np.mean(rand_s_list) + (3 * np.std(rand_s_list))  # threshold = mean + 3stdev

    db_scores = getScores(db, score, residue_dict)
    novel_homologs = [x for x in db_scores if x[1] >= threshold]

    return novel_homologs, rand_s_list


db, fam, transition_matrix, residue_dict = loadData(sys.argv[1], sys.argv[2], sys.argv[3])    

nov_homs, randDB_scores = findHomologs(db, fam, transition_matrix, residue_dict)

out_file = raw_input('Name of output file: ')

with open(out_file, 'w') as f:
    for tup in nov_homs:
        count = 0
        for s in randDB_scores:
            if s >= tup[1]:
                count += 1
        p_val = float(count) / len(nov_homs)

        f.write(tup[0] + '\t' + str(tup[1]) + '\t' + str(p_val) + '\n')

