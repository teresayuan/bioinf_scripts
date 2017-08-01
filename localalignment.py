# Local alignment
# python locAL.py <seq file> -m <match> -s <mismatch> -d <indel> -a
# Takes in a file of sequence pairs; scores of matches, mismatches, and 
# insertion/deletions; if alignment should be printed or not
# Uses dynamic programming to find the highest scoring local alignment

import sys

def localAlignment(s1, s2, match_score, mismatch_score, indel_score):

    S = []
    backtrack = []
    max_val = -1

    num_rows = len(s1)+1
    num_cols = len(s2)+1

    # initialize first row and column to 0
    for i in range(num_rows):
        row = [0] * num_cols
        back_row = ['0'] * num_cols

        S.append(row)
        backtrack.append(back_row)

    for i in range(1, num_rows):
        for j in range(1, num_cols):

            S[i][j] = max(0, S[i-1][j-1] + (match_score if s1[i-1] == s2[j-1] else mismatch_score),
                          S[i-1][j] + indel_score, S[i][j-1] + indel_score)

            if S[i][j] > max_val:
                max_val = S[i][j]
                max_index = (i,j)

            if S[i][j] == 0:
                backtrack[i][j] = '0'
            elif S[i][j] == S[i-1][j-1] + (match_score if s1[i-1] == s2[j-1] else mismatch_score):
                backtrack[i][j] = 'diagonal'
            elif S[i][j] == S[i-1][j]+indel_score:
                backtrack[i][j] = 'vertical'
            elif S[i][j] == S[i][j-1]+indel_score:
                backtrack[i][j] = 'horizontal'

    return S, backtrack, max_index

def outputLocalAlignment(s1, s2, backtrack, max_index):
    a1 = ''
    a2 = ''

    i = max_index[0]
    j = max_index[1]

    while True:

        if backtrack[i][j] == '0':
            if i == 0 and j!= 0:
                a1 = '-' + a1
                a2 = s2[j-1] + a2
            elif i != 0 and j == 0:
                a1 = s1[i-1] + a1
                a2 = '-' + a2
            else:
                a1 = s1[i-1] + a1
                a2 = s2[j-1] + a2
            break
        elif backtrack[i][j] == 'diagonal':
            if i == 0:
                a1 = '-' + a1
                a2 = s2[j-1] + a2
            elif j == 0:
                a1 = s1[i-1] + a1
                a2 = '-' + a2
            else:
                a1 = s1[i-1] + a1
                a2 = s2[j-1] + a2
            i = i - 1
            j = j - 1
        elif backtrack[i][j] == 'vertical':
            a1 = s1[i-1] + a1
            a2 = '-' + a2
            i = i - 1
        elif backtrack[i][j] == 'horizontal':
            a1 = '-' + a1
            a2 = s2[j-1] + a2
            j = j - 1

    return a1, a2

def part2(seq_file, match_score, mismatch_score, indel_score):
    lines = [line.rstrip('\n') for line in open(seq_file)]

    align_lengths = []

    for i in range(0, 1000, 2):
        s1 = lines[i]
        s2 = lines[i+1]

        S, backtrack, max_index = localAlignment(s1, s2, match_score, mismatch_score, indel_score)
        a1, a2 = outputLocalAlignment(s1, s2, backtrack, max_index)

        if (i/2)%50 == 0:
            print str(i/2)

        align_lengths.append(len(a1))

    return align_lengths


if len(sys.argv) < 8:
    print "Incorrect command line arguments. Try again."
    print "python locAL.py <seq file> -m <match> -s <mismatch> -d <indel> -a"
    sys.exit()

seq_file = sys.argv[1]
match_score = int(sys.argv[3])
mismatch_score = int(sys.argv[5])
indel_score = int(sys.argv[7])
if len(sys.argv) == 9 and sys.argv[8] == '-a':
    out_align = True
else:
    out_align = False


lines = [line.rstrip('\r\n') for line in open(seq_file)]

s1 = lines[1]
s2 = lines[4]

S, backtrack, max_index = localAlignment(s1, s2, match_score, mismatch_score, indel_score)
a1, a2 = outputLocalAlignment(s1, s2, backtrack, max_index)


#print 'where is highest score? --> ' + str(max_index)

print 'Score of best alignment --> ' + str(S[max_index[0]][max_index[1]])
print 'Length of best alignment --> ' + str(len(a1))

# print 'SCORE MATRIX: '
# for row in S:
#     print row
#
# print 'BACKTRACK MATRIX:'
# for row in backtrack:
#     print row

if out_align:
    print a1
    print a2
