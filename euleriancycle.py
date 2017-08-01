# Eulerian Cycle 
# Finds an eulerian cycle in the graph

# Sample Dataset
# 0 -> 3
# 1 -> 0
# 2 -> 1,6
# 3 -> 2
# 4 -> 2
# 5 -> 4
# 6 -> 5,8
# 7 -> 9
# 8 -> 7
# 9 -> 6

# Sample Output
# 6->8->7->9->6->5->4->2->1->0->3->2->6

import random
import copy

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


textFile = raw_input('Name of input file: ')

graph = {}

with open(textFile) as f:
    for line in f:
        line = line.strip('\n')
        (key, val) = line.split(' -> ')
        list = val.split(',')
        list = [int(i) for i in list]
        graph[int(key)] = list


eCycle = eulerianCycle(graph)

outFile = raw_input('Name of output file: ')

file = open(outFile, 'w')

for node in range(0, len(eCycle)):
    if node == len(eCycle)-1:
        file.write('%s' % (eCycle[node]))
    else:
        file.write('%s->' % (eCycle[node]))

file.close()