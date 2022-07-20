import math
import itertools


from scipy.optimize import linprog

#number of points
n = 6
distances = [[0 for x in range(n)] for y in range(n)]

#LHS dij >= 1
A = []
B = []
id = [[0 for x in range(n)] for y in range(n)]
for i in range(math.comb(n,2)):
    x = [0 for x in range(math.comb(n,2))]
    x[i] = -1
    A.append(x)
    B.append(-1)

count = 0
for x in range(n):
    for y in range(x+1, n):
        id[x][y] = count
        id[y][x] = count
        count += 1

#LHS dik + dkj >= dij
for i in range(n):
    for j in range(i+1, n):
        for k in range(n):
            if k != i and i != j and k != j:
                x = [0 for x in range(math.comb(n,2))]
                x[id[i][k]] = -1
                x[id[k][j]] = -1
                x[id[i][j]] = 1
                A.append(x)
                B.append(0)

#create all possible matchings
allMatchings = []
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

generate_matching(n, 0, [-1 for x in range(n)])

#define the first matching to be the maximum matching
maxMatch = allMatchings[0]
for match in allMatchings:
    x = [0 for x in range(math.comb(n, 2))]
    for i in range(n):
        x[id[i][match[i]]] += 1
        x[id[i][maxMatch[i]]] += -1
    A.append(x)
    B.append(0)

#define paterns needed to iterate over all possible detour points
patterns = []
cut = 0
for i in range(n):
    pattern = []
    x = []
    for j in range(n):
        if i != j and i != maxMatch[j]:
            x.append(j)
            cut = cut + 1
        if cut == 2:
            pattern.append(x)
            x = []
            cut = 0
    patterns.append(pattern)

lst = list(itertools.product([x for x in range(int((n-2)/2))], repeat=n))
alpha = 3
#define the constraints for every permutation resulting in different LPs to solve
def createConstraintsForPermutation(perm):
    Afinal = A.copy()
    for i in range(n):
        x = [0 for _ in range(math.comb(n, 2))]
        point1 = patterns[i][perm[i]][0]
        point2 = patterns[i][perm[i]][1]
        x[id[point1][i]] = -1
        x[id[i][point2]] = -1
        x[id[point1][point2]] = alpha
        Afinal.append(x)
    return Afinal


increment = 2
incremented = False
for _ in range(n):
    B.append(0)
C = []
for i in range(math.comb(n, 2)):
    C.append(0)

foundMetricForEveryPattern = True

#binary search for alpha
for i in range(10):
    for el in lst:
        Afinal = createConstraintsForPermutation(el)
        res = linprog(C, A_ub=Afinal, b_ub=B, options = {'lstsq': True})
        if res.status == 2: #status == 2 if problem is infeasible
            foundMetricForEveryPattern = False
    if foundMetricForEveryPattern:
        alpha = alpha + increment
        increment = increment * 3 / 4
        print(alpha)
    else:
        alpha = alpha - increment
        increment = increment * 3 / 4
        print(alpha)
    foundMetricForEveryPattern = True

# Print results
print('Optimal value:', round(res.fun*-1, ndigits=2),
      '\nx values:', res.x,
      '\nNumber of iterations performed:', res.nit,
      '\nStatus:', res.message)




