# Maximal Non-Branching Pattern
# Finds all maximal non-branching paths in the graph

# Sample Dataset
# 1 -> 2
# 2 -> 3
# 3 -> 4,5
# 6 -> 7
# 7 -> 6

# Sample Output
# 1 -> 2 -> 3
# 3 -> 4
# 3 -> 5
# 7 -> 6 -> 7

import random
import copy

def findDegrees(graph):
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

    return inDegree, outDegree

def makeCycle(start, graph):
    cycleList = [start]

    nextNode = random.choice(graph[start])
    graph[start].remove(nextNode)

    cycleList.append(nextNode)

    currNode = nextNode

    while currNode != start:
        if currNode not in graph.keys():
            return -1

        currNodeList = graph[currNode]

        if len(currNodeList) == 0:
            return -1
        nextNode = random.choice(currNodeList)
        cycleList.append(nextNode)

        graph[currNode].remove(nextNode)

        currNode = nextNode

    return cycleList

def maximalNonBranchingPaths(graph):

    inDegree, outDegree = findDegrees(graph)
    print inDegree
    print outDegree

    paths = []

    for v in graph.keys():
        print v
        #node = graph[v]
        if not (inDegree[v] == 1 and outDegree[v] == 1):
            if outDegree[v] > 0:
                for w in graph[v]:
                    nonBranchingPath = [v, w]

                    while inDegree[w] == 1 and outDegree[w] == 1:
                        u = graph[w][0]
                        nonBranchingPath.append(u)
                        w = u

                    paths.append(nonBranchingPath)

    visited = set()

    for node in graph.keys():
        counter = 0
        if node not in visited:
            cycle = makeCycle(node, copy.deepcopy(graph))

            if cycle != -1:
                for n in range(0, len(cycle)):
                    inode = cycle[n]
                    visited.add(inode)
                    if (inDegree[inode] == 1 and outDegree[inode] == 1):
                        counter += 1

                if counter == len(cycle):
                    paths.append(cycle)

    return paths

textFile = raw_input('Name of input file: ')

graph = {}

with open(textFile) as f:
    for line in f:
        line = line.strip('\n')
        (key, val) = line.split(' -> ')
        list = val.split(',')
        list = [int(i) for i in list]
        graph[int(key)] = list

# print graph

# print maximalNonBranchingPaths(graph)

paths = maximalNonBranchingPaths(graph)

outFile = raw_input('Name of output file: ')

file = open(outFile, 'w')

for i in range(0, len(paths)):
    for node in range(0, len(paths[i])):
        if node == len(paths[i])-1:
            file.write('%s\n' % (paths[i][node]))
        else:
            file.write('%s->' % (paths[i][node]))

file.close()