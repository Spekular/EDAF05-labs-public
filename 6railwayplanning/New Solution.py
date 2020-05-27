import copy
import gc
import time

#Get number of [nodes, edges, minimum capacity, routes to remove]
myArgs = list(map(int, input().split()))
numNodes = myArgs[0]
numEdges = myArgs[1]
requiredFlow = myArgs[2]
maxRemovals = myArgs[3]

#Debug helpers
debugStrings = []
def debug(message):
	debugStrings.append(message)

def printDebugs():
	for message in debugStrings: print(message)

def debugEdgeGraph(matrix):
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

#Position [x][y] gives initial capacity of edge x -> y
initialCapacity = [row[:] for row in edgeTemplate]
for i in range(0, numEdges):
	(start, end, cost) = route[i]
	#Edges are undirected
	initialCapacity[start][end] = cost
	initialCapacity[end][start] = cost
mutableCapacity = [row[:] for row in initialCapacity]

#Initial neigbors, nodes with a capacity of >0 between themselves
initialNeighbors = [[] for i in range (0, numNodes)]
for i in range(0, numNodes):
	for j in range(0, numNodes):
		if (i == j): continue
		if (initialCapacity[i][j] > 0): initialNeighbors[i].append(j)
mutableNeighbors = [row[:] for row in initialNeighbors]

#Order in which we want to remove routes
removeQueue = [int(input()) for i in range (0, maxRemovals)]

#
def reducedCapacity(num):
	capacity = [row[:] for row in initialCapacity]
	neighbors = [row[:] for row in initialNeighbors]

	for i in range(0, num):
		(start, end, x) = route[removeQueue[i]]
		capacity[start][end] = 0
		capacity[end][start] = 0
		neighbors[start].remove(end)
		neighbors[end].remove(start)
	return (capacity, neighbors)

def removeEdge(removal):
	(start, end, x) = route[removal]
	mutableCapacity[start][end] = 0
	mutableCapacity[end][start] = 0
	mutableNeighbors[start].remove(end)
	mutableNeighbors[end].remove(start)

#Premade stuff for findMaxFlow,m
#copying seems to be ~10 times faster than remaking the lists
predTemplate = [i for i in range (0, numNodes)]
visitedTemplate = [False for i in range (0, numNodes)]
visitedTemplate[0] = True

def findMaxFlow(capacity, neighbors):
	flow = [row[:] for row in edgeTemplate]
	sink = numNodes - 1

	theoreticalMax = sum(capacity[0])
	initialMinCap = 1
	while (initialMinCap < theoreticalMax):
		initialMinCap = initialMinCap * 2

	def increaseFlow(minCap):
		pathFound = False
		pred = predTemplate[:]
		visited = visitedTemplate[:]
		remaining = []

		for i in neighbors[0]:
			cap = capacity[0][i] - flow[0][i]
			if (cap > minCap): remaining.append(i)
			pred[i] = 0

		while remaining:
			node = remaining.pop(0)
			visited[node] = True

			if node == sink:
				pathFound = True
				break

			for i in neighbors[node]:
				if (visited[i]): continue
				cap = capacity[node][i] - flow[node][i]
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
			flowLimit = capacity[pred[sink]][sink] - flow[pred[sink]][sink]
			node = sink
			while node > 0:
				cap = capacity[pred[node]][node] - flow[pred[node]][node]
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
	capacity = [row[:] for row in initialCapacity]
	neighbors = [row[:] for row in initialNeighbors]

	removedEdges = 0
	start = time.time()
	maxFlow = findMaxFlow(capacity, neighbors)

	#for i in range(1, maxRemovals+1):
	#	(capacity, neighbors) = reducedCapacity(i)
	#	newMaxFlow = findMaxFlow(capacity, neighbors)
	#	gc.collect()
	#	if (newMaxFlow >= requiredFlow):
	#		removedEdges += 1
	#		maxFlow = newMaxFlow
	#	else:
	#		break
	for r in removeQueue:
		removeEdge(r)
		newMaxFlow = findMaxFlow(mutableCapacity, mutableNeighbors)
		gc.collect()

		if (newMaxFlow >= requiredFlow):
			removedEdges += 1
			maxFlow = newMaxFlow
			#print(str(time.time() - start) + " seconds after start:")
			#print("  Found solution with " + str(removedEdges) + " removed edges")
		else:
			break

	return (removedEdges, maxFlow)

(removals, maxFlow) = optimizeRailways()
print(str(removals) + " " + str(maxFlow))
printDebugs()
