# k-Universal Circular String 
# Return a k-universal circular string

# Sample Dataset
# 4

# Sample Output
# 0000110010111101

import random
import copy

def getPrefix(pattern):
    return pattern[:-1]

def getSuffix(pattern):
    return pattern[1:]

def lastSymbol(pattern):
    return pattern[-1]

def deBruijnPatt(patterns):

    edges = patterns

    nodes = {}

    for i in range(0, len(edges)):
        nodes[getPrefix(edges[i])] = []

    for i in range(0, len(edges)):
        nodes[getPrefix(edges[i])].append(getSuffix(edges[i]))
        nodes[getPrefix(edges[i])].sort()

    return nodes

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

def eulerianCycle(graph):

    while True:
        randStart = random.choice(graph.keys())
        cycle, newGraph = makeCycle(randStart, copy.deepcopy(graph))

        if cycle != -1:
            break

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

def getBinaryKmers(k):
    kmersList = []

    for i in range(1 << k):
        num = bin(i)[2:]
        num = '0' * (k - len(num)) + num
        kmersList.append(num)

    return kmersList

def kUniCircularStrings(k):

    kmersList = getBinaryKmers(k)

    kmerDict = deBruijnPatt(kmersList)


    cycle = eulerianCycle(kmerDict)

    string = list(cycle[0])

    for i in range(1, len(cycle)):
        if getSuffix(cycle[i - 1]) == getPrefix(cycle[i]):
            string.append(lastSymbol(cycle[i]))

    string = string[:-(k-1)]

    return string

textFile = raw_input('Input Text File: ')

lines = [line.rstrip('\n') for line in open(textFile)]

k = int(lines[0])

print ''.join(kUniCircularStrings(k))