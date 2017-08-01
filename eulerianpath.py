# Eulerian Path
# Finds an Eulerian path in this graph

# Sample Dataset
# 0 -> 2
# 1 -> 3
# 2 -> 1
# 3 -> 0,4
# 6 -> 3,7
# 7 -> 8
# 8 -> 9
# 9 -> 6

# Sample Output
# 6->7->8->9->6->3->0->2->1->3->4

import random
import copy

def findUnbalance(graph):
    inDegree = {}
    outDegree = {}

    # Initialize inDegree and outDegree dictionaries to 0
    for i in range(0, (max(graph.keys())+1)):
        inDegree[i] = 0
        outDegree[i] = 0

    # Fill outDegree
    for node, nodeList in graph.items():
        outDegree[node] = len(nodeList)

    # Fill inDegree
    for node, nodeList in graph.items():
        for dest in nodeList:
            inDegree[dest] += 1

    print inDegree
    print outDegree

    for i in range(0, len(inDegree)):
        if inDegree[i] != outDegree[i]:
            if inDegree[i] > outDegree[i]:
                end = i
                #print 'end -> ' + str(end) + '; in- ' + str(inDegree[i]) + ', out- ' + str(outDegree[i])
            elif inDegree[i] < outDegree[i]:
                start = i
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


textFile = raw_input('IName of input file: ')

graph = {}

with open(textFile) as f:
    for line in f:
        line = line.strip('\n')
        (key, val) = line.split(' -> ')
        list = val.split(',')
        list = [int(i) for i in list]
        graph[int(key)] = list

print graph

ePath = eulerianPath(graph)

outFile = raw_input('Name of output file: ')

file = open(outFile, 'w')

for node in range(0, len(ePath)):
    if node == len(ePath)-1:
        file.write('%s' % (ePath[node]))
    else:
        file.write('%s->' % (ePath[node]))

file.close()