import sys
from queue import Queue
import itertools

debug = False

n = 6

matrices = []
allMatchings = []

readMatrix = False
currentMatrix = []
currentRow = []
readEntries = 0
readRows = 0
shouldRead = False
readMatrixCounter = 1


with open("n6.txt") as f:
    for c in itertools.chain.from_iterable(f):
        if c == '.':
            shouldRead = True
        elif c == 'G':
            shouldRead = False
        if c.isdigit() and shouldRead:
            if readEntries == n:
                currentMatrix.append(currentRow)
                readRows = readRows + 1
                currentRow = [int(c)]
                readEntries = 1
            else:
                currentRow.append(int(c))
                readEntries = readEntries + 1
            if readRows == n:
                matrices.append(currentMatrix)
                currentMatrix = []
                readRows = 0
                readEntries = 1
                print("read: ", readMatrixCounter+1, " / 11117", )
                readMatrixCounter = readMatrixCounter + 1
#append last matrix
currentMatrix.append(currentRow)
matrices.append(currentMatrix)


def matrixToList(matrix):
    adjList = []
    for i in range(n):
        list = []
        for j in range(n):
            if matrix[i][j] == 1:
                list.append(j)
        adjList.append(list)
    return adjList

def getDistances(i, adjList):
    Q = Queue()
    distance = [sys.maxsize for i in range(n)]
    Q.put(i)
    visitedVertices = set()
    visitedVertices.update({i})
    while not Q.empty():
        node = Q.get()
        if node == i:
            distance[node] = 0
        for u in adjList[node]:
            if u not in visitedVertices:
                if distance[u] > distance[node] + 1:
                    distance[u] = distance[node] + 1
                Q.put(u)
                visitedVertices.update({u})
    return distance

def computeMetricFromAdjList(adjList):
    metric = [[0 for _ in range(n)] for _ in range(n)]
    distances = [[] for _ in range(n)]
    for i in range(n):
        distances[i] = getDistances(i, adjList)
    for i in range(n):
        for j in range(n):
            metric[i][j] = distances[i][j]
    return metric

def generate_matching (n, currentindex, matched):
    if currentindex == n:
        allMatchings.append(matched.copy())
        return
    if matched[currentindex] != -1:
        generate_matching(n, currentindex + 1, matched)
        return
    for i in range(currentindex+1, n):
        if matched[i] == -1:
            matched[currentindex] = i
            matched[i] = currentindex
            generate_matching(n, currentindex+1, matched)
            matched[currentindex] = -1
            matched[i] = -1

def computeMaxMatchings(metric):
    maxDist = 0
    maxMatches = []
    for match in allMatchings:
        dist = 0
        for i in range(n):
            dist = dist + metric[i][match[i]]
        if dist > maxDist:
            maxDist = dist
    for match in allMatchings:
        dist = 0
        for i in range(n):
            dist = dist + metric[i][match[i]]
        if dist >= maxDist:
            maxMatches.append(match)
    return maxMatches

def computeAlphaDetour(matching, metric):
    alpha = sys.maxsize
    detourPoint = -1

    for i in range(n):
        maxAlpha = 0
        for j in range(n):
            if j != i and matching[j] != i:
                detour = (metric[j][i] + metric[i][matching[j]]) / metric[j][matching[j]]
                if detour > maxAlpha:
                    maxAlpha = detour
        if maxAlpha < alpha:
            alpha = maxAlpha
            detourPoint = i
    return (alpha, detourPoint)


def computeMatchingWithBiggestDetour(metric, maxMatchings):
    maxAlpha = sys.maxsize
    finalDetourPoint = -1
    finalMatching = maxMatchings[0]
    for matching in maxMatchings:
        (alpha, detourPoint) = computeAlphaDetour(matching, metric)
        if alpha < maxAlpha:
            maxAlpha = alpha
            finalDetourPoint = detourPoint
            finalMatching = matching
    return (finalMatching, maxAlpha, finalDetourPoint)

maxAlpha = 0
theMatrix = []
theMetric = []
theMaxMatchings = []
theMaxMatching = []
theDetourPoint = -1
generate_matching(n, 0, [-1 for x in range(n)])
analysedMatrixCounter = 1

for matrix in matrices:
    print("analysed: ", analysedMatrixCounter, " / ", len(matrices))
    analysedMatrixCounter = analysedMatrixCounter + 1
    adjList = matrixToList(matrix)
    metric = computeMetricFromAdjList(adjList)
    maxMatchings = computeMaxMatchings(metric)
    (matching, alpha, detourPoint) = computeMatchingWithBiggestDetour(metric, maxMatchings)
    if alpha > maxAlpha:
        maxAlpha = alpha
        theMatrix = matrix
        theMetric = metric
        theMaxMatchings = maxMatchings
        theMaxMatching = matching
        theDetourPoint = detourPoint

print("----MATRIX----")
for line in theMatrix:
    print(line)
print("----ADJACENCY LIST----")
print(matrixToList(theMatrix))
print("----METRIC----")
for line in theMetric:
    print(line)
print("----MAXMATCHINGS----")
print(theMaxMatchings)
print("----MAXMATCHING WITH BIGGEST DETOUR----")
print(theMaxMatching)
print("----ALPHA----")
print(maxAlpha)
print("----DETOUR POINT----")
print(theDetourPoint)

