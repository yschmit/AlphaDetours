import math
import random
import sys

n = 6
height = 100
width = 100
allMatchings = []

def distance(x, y):
    (a,b) = x
    (c,d) = y
    return math.sqrt(((a-c)*(a-c)) + (b-d)*(b-d))

def createRandomPoints(n):
    points = []
    for i in range(n):
        x = random.randint(0, width)
        y = random.randint(0, height)
        points.append((x,y))
    return points

def createMetric(points):
    metric = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            metric[i][j] = distance(points[i], points[j])
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

def computeAlphaDetour(matching, points):
    smallestAlpha = sys.maxsize
    finalDetourPoint = (0,0)
    minX = sys.maxsize
    maxX = 0
    minY = sys.maxsize
    maxY = 0
    for point in points:
        (x,y) = point
        if x < minX:
            minX = x
        if x > maxX:
            maxX = x
        if y < minY:
            minY = y
        if y > maxY:
            maxY = y
    for x in range(minX, maxX+1):
        for y in range(minY, maxY+1):
            detourPoint = (x, y)
            highestDetour = 0
            for k in range(n):
                detour = (distance(points[k], detourPoint) + distance(detourPoint, points[matching[k]])) / (distance(points[k], points[matching[k]]))
                if detour > highestDetour:
                    highestDetour = detour
            if highestDetour < smallestAlpha:
                smallestAlpha = highestDetour
                finalDetourPoint = detourPoint
    return (smallestAlpha, finalDetourPoint)

def computeMatchingWithBiggestDetour(maxMatchings, points):
    maxAlpha = 0
    finalDetourPoint = 0
    finalMatching = maxMatchings[0]
    for matching in maxMatchings:
        (alpha, detourPoint) = computeAlphaDetour(matching, points)
        if alpha > maxAlpha:
            maxAlpha = alpha
            finalDetourPoint = detourPoint
            finalMatching = matching
    return (finalMatching, maxAlpha, finalDetourPoint)

generate_matching(n, 0, [-1 for x in range(n)])

maxAlpha = 0
for i in range(1):
    points = [(-10,-10), (-20,-5), (-15,25), (-5,5), (5,-20), (20,0)]
    metric = createMetric(points)
    maxMatchings = computeMaxMatchings(metric)
    (matching, alpha, detourPoint) = computeMatchingWithBiggestDetour(maxMatchings, points)
    if alpha > maxAlpha:
        print(matching)
        print(alpha)
        print(detourPoint)
        maxAlpha = alpha