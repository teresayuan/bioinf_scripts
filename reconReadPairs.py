# Sequence Reconstruction from Read-Pairs
# Given integers k and d and a collection of paired k-mers PairedReads.
# Return a string with (k, d)-mer composition equal to PairedReads

# Sample Dataset
# 4 2
# GAGA|TTGA
# TCGT|GATG
# CGTG|ATGT
# TGGT|TGAG
# GTGA|TGTT
# GTGG|GTGA
# TGAG|GTTG
# GGTC|GAGA
# GTCG|AGAT

# Sample Output
# GTGGTCGTGAGATGTTGA

import random
import copy

def lastSymbol(pattern):
    return pattern[-1]

def getPrefix(pattern):
    return pattern[:-1]

def getSuffix(pattern):
    return pattern[1:]

def modDeBruijnPatt(pairedPatterns):

    edges = pairedPatterns

    nodes = {}

    for i in range(0, len(edges)):
        pattern1 = edges[i][0]
        pattern2 = edges[i][1]
        prefix = (getPrefix(pattern1), getPrefix(pattern2))
        nodes[prefix] = []

    for i in range(0, len(edges)):
        pattern1 = edges[i][0]
        pattern2 = edges[i][1]
        prefix = (getPrefix(pattern1), getPrefix(pattern2))
        suffix = (getSuffix(pattern1), getSuffix(pattern2))
        nodes[prefix].append(suffix)
        nodes[prefix].sort()

    return nodes

def findUnbalance(graph):
    inDegree = {}
    outDegree = {}

    # Initialize inDegree and outDegree dictionaries to 0
    possibleVals = set()
    possibleVals.update(graph.keys())

    for node in graph.keys():
        possibleVals.update(graph[node])

    for patt in possibleVals:
        inDegree[patt] = 0
        outDegree[patt] = 0

    # Fill outDegree
    for node, nodeList in graph.items():
        outDegree[node] = len(nodeList)

    # Fill inDegree
    for node, nodeList in graph.items():
        for dest in nodeList:
            inDegree[dest] += 1

    print inDegree
    print outDegree

    for key in possibleVals:
        if inDegree[key] != outDegree[key]:
            if inDegree[key] > outDegree[key]:
                end = key
                #print 'end -> ' + str(end) + '; in- ' + str(inDegree[i]) + ', out- ' + str(outDegree[i])
            elif inDegree[key] < outDegree[key]:
                start = key
                #print 'start -> ' + str(start) + '; in- ' + str(inDegree[i]) + ', out- ' + str(outDegree[i])

    return start, end

def makeCycle(start, graph):
    cycleList = [start]

    nextNode = random.choice(graph[start])
    graph[start].remove(nextNode)

    cycleList.append(nextNode)

    currNode = nextNode

    while currNode != start:
        currNodeList = graph[currNode]

        if len(currNodeList) == 0:
            return -1
        nextNode = random.choice(currNodeList)
        cycleList.append(nextNode)

        graph[currNode].remove(nextNode)

        currNode = nextNode

    return cycleList, graph

def unexplored(graph):
    flag = True
    counter = 0

    for node, edgeList in graph.items():
        if len(edgeList) == 0:
            counter += 1

    # No more unexplored edges
    if counter == len(graph):
        flag = False

    return flag

def modEulerianCycle(graph, start):
    cycle, newGraph = makeCycle(start, copy.deepcopy(graph))

    # print cycle
    # print newGraph
    # print unexplored(newGraph)

    while unexplored(newGraph):
        for node in cycle:
            if len(newGraph[node]) != 0:
                newStart = node
                break

        newCycle = []

        startIndex = cycle.index(newStart)

        tempCycle, newGraph = makeCycle(newStart, copy.deepcopy(newGraph))

        newCycle = cycle[:startIndex] + tempCycle + cycle[startIndex+1:]

        cycle = newCycle

    return cycle

def eulerianPath(graph):
    start, end = findUnbalance(graph)

    # print 'start = ' + str(start)
    # print 'end = ' + str(end)

    graph[end] = [start]

    cycle = modEulerianCycle(copy.deepcopy(graph), start)

    snip = cycle.index(end)

    path = cycle[snip+1:-1] + cycle[:snip+1]

    return path

def pairedReconString(pairedPatterns, k, d):
    DBDict = modDeBruijnPatt(pairedPatterns)

    path = eulerianPath(DBDict)

    # print DBDict
    # print path

    p1 = []
    p2 = []
    for i in range(0, len(path)):
        p1.append(path[i][0])
        p2.append(path[i][1])

    prefixString = list(p1[0])
    for i in range(1, len(p1)):
        if getSuffix(p1[i - 1]) == getPrefix(p1[i]):
            prefixString.append(lastSymbol(p1[i]))

    suffixString = list(p2[0])
    for i in range(1, len(p2)):
        if getSuffix(p2[i - 1]) == getPrefix(p2[i]):
            suffixString.append(lastSymbol(p2[i]))

    # print prefixString
    # print suffixString

    string = prefixString + suffixString[-(k+d):]

    return string

textFile = raw_input('Name of input file: ')

lines = [line.rstrip('\n') for line in open(textFile)]

variables = lines[0].split()
k = int(variables[0])
d = int(variables[1])

pairedPatterns = []

for i in range(1, len(lines)):
    pairedPatterns.append(lines[i].split('|'))

reconString = pairedReconString(pairedPatterns, k, d)

outFile = raw_input('Name of output file: ')

f = open(outFile, 'w')

f.write(''.join(reconString))

f.close()