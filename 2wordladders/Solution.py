#Get number of words and queries
intArgs = list(map(int, input().split()))

numWords = intArgs[0]
numQueries = intArgs[1]

#Populate list of words
words = []

for i in range(0, numWords):
	words.append(input().split()[0])

wordIndex = dict(zip(words, range(0,len(words))))

#Generate graph edges. neighbors[0] contains all directed edges 0 -> e
neighbors = []

for i in range(0, numWords):
	lastFour = words[i][1:5]
	letterCount = map(lastFour.count, lastFour)
	letterDict = dict(zip(lastFour, letterCount))

	edges = []
	for j in range(0, numWords):
		if i == j: continue
		candidate = words[j]
		if all(
			candidate.count(letter) >= letterDict.get(letter)
			for letter in lastFour
		):
			edges.append(j)

	neighbors.append(edges)

#Populate list of queries
queries = []

for i in range(0, numQueries):
	queries.append(input().split())

#TODO: Find paths
def findPath(start, goal):
	if start == goal:
		print("0", end ="\r\n")
		return
	#Initialize
	visited = []
	for i in range(0, numWords): visited.append(False)
	visited[start] = True

	pred = []
	for i in range(0, numWords): pred.append(-1)

	pathFound = False

	remaining = [start]

	while remaining:
		node = remaining.pop(0)
		for next in neighbors[node]:
			if not visited[next]:
				visited[next] = True
				remaining.append(next)
				pred[next] = node
				if next == goal:
					pathFound = True
					break

	length = -1
	if pathFound:
		node = goal
		while node >= 0:
			node = pred[node]
			length += 1

	if length >= 0: print(length, end ="\r\n")
	else: print("Impossible", end ="\r\n")

for q in range(0, numQueries):
	query = queries[q]
	start = wordIndex.get(query[0])
	goal = wordIndex.get(query[1])

	findPath(start, goal)
