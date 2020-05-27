import copy
import gc

#Get number of [nodes, edges, minimum capacity, routes to remove]
myArgs = list(map(int, input().split()))
numNodes = myArgs[0]
numEdges = myArgs[1]
requiredFlow = myArgs[2]
numRemovals = myArgs[3]

#Debug helpers
debugStrings = []
debugEnabled = False
def debug(message):
	if debugEnabled:
		debugStrings.append(message)
		#print(message)
def printDebugs():
	for message in debugStrings: print(message)
def printCapacities(matrix):
	for i in range (0, numNodes):
		for j in range(0, numNodes):
			debug(str(i) + " -> " + str(j) + ": " + str(matrix[i][j]))

#Routes: keep them around in input order so we can remove them by index later
route = [(0,0,0) for i in range(0, numEdges)]
for i in range(0, numEdges):
	values = list(map(int, input().split()))
	route[i] = (values[0], values[1], values[2])

#Template array for listing edge values, 2~3 times faster than recreating each time
edgeTemplate = [[0 for x in range(0, numNodes)] for y in range(0, numNodes)]
#Edges: Routes in a format that's nicer to work with,
#Position [x][y] gives capacity of edge x -> y
capacityOf = [row[:] for row in edgeTemplate]
for i in range(0, numEdges):
	(start, end, cost) = route[i]
	#Edges are undirected
	capacityOf[start][end] = cost
	capacityOf[end][start] = cost

#Neighbors
neighbors = [[] for i in range (0, numNodes)]
for i in range(0, numNodes):
	for j in range(0, numNodes):
		if (i == j): continue
		if (capacityOf[i][j] > 0): neighbors[i].append(j)


#Order in which we want to remove routes
removeQueue = [int(input()) for i in range (0, numRemovals)]

#Premade stuff, copying seems to be ~10 times faster than remaking the lists
predTemplate = [i for i in range (0, numNodes)]
visitedTemplate = [False for i in range (0, numNodes)]
visitedTemplate[0] = True

def removeEdge(removal):
	(start, end, capacity) = route[removal]
	capacityOf[start][end] = 0
	capacityOf[end][start] = 0
	neighbors[start].remove(end)
	neighbors[end].remove(start)

def findMaxFlow():
	flow = [row[:] for row in edgeTemplate]
	sink = numNodes - 1

	theoreticalMax = sum(capacityOf[0])
	initialMinCap = 1
	while (initialMinCap < theoreticalMax):
		initialMinCap = initialMinCap * 2

	def increaseFlow(minCap):
		pathFound = False
		pred = predTemplate[:]
		visited = visitedTemplate[:]
		remaining = []

		for i in neighbors[0]:
			cap = capacityOf[0][i] - flow[0][i]
			if (cap > 0): remaining.append(i)
			pred[i] = 0

		while remaining:
			node = remaining.pop(0)
			visited[node] = True

			if node == sink:
				pathFound = True
				break

			for i in neighbors[node]:
				if (visited[i]): continue
				cap = capacityOf[node][i] - flow[node][i]
				if (cap < minCap): continue

				visited[i] = True
				remaining.append(i)
				pred[i] = node

				if i == sink:
					remaining = []
					pathFound = True
					break

		flowLimit = 0
		if pathFound:
			flowLimit = capacityOf[pred[sink]][sink] - flow[pred[sink]][sink]
			node = sink
			while node > 0:
				cap = capacityOf[pred[node]][node] - flow[pred[node]][node]
				flowLimit = min(flowLimit, cap)
				node = pred[node]

			node = sink
			while node > 0:
				flow[node][pred[node]] -= flowLimit
				flow[pred[node]][node] += flowLimit
				node = pred[node]

		return flowLimit

	currentMinCap = initialMinCap*2
	while (currentMinCap > 1):
		currentMinCap = int(currentMinCap / 2)
		flowIncrease = increaseFlow(currentMinCap)
		while (flowIncrease > 0):
			flowIncrease = increaseFlow(currentMinCap)

	#Everything that flows out of the source must reach the sink
	return sum(flow[0])

def optimizeRailways():
	removedEdges = 0
	maxFlow = findMaxFlow()

	for r in removeQueue:
		removeEdge(r)
		newMaxFlow = findMaxFlow()
		gc.collect()
		if (newMaxFlow >= requiredFlow):
			removedEdges += 1
			maxFlow = newMaxFlow
		else:
			break

	return (removedEdges, maxFlow)

if (numNodes >= 5): debugEnabled = True
(numRemovals, finalMaxFlow) = optimizeRailways()
print(str(numRemovals) + " " + str(finalMaxFlow))
#printDebugs()
