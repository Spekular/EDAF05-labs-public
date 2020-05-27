import copy
import gc

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
initialCapacity = [row[:] for row in edgeTemplate]
for i in range(0, numEdges):
	(start, end, cost) = route[i]
	#Edges are undirected
	initialCapacity[start][end] = cost
	initialCapacity[end][start] = cost

#Neigbors, nodes with a capacity of >0 between themselves
initialNeighbors = [[] for i in range (0, numNodes)]
for i in range(0, numNodes):
	for j in range(0, numNodes):
		if (i == j): continue
		if (initialCapacity[i][j] > 0): initialNeighbors[i].append(j)


#Order in which we want to remove routes
removeQueue = [int(input()) for i in range (0, maxRemovals)]

#Premade stuff, copying seems to be ~10 times faster than remaking the lists
predTemplate = [i for i in range (0, numNodes)]
visitedTemplate = [False for i in range (0, numNodes)]
visitedTemplate[0] = True

def reducedCapacity(numRemovals):
	capacity = [row[:] for row in initialCapacity]
	neighbors = [row[:] for row in initialNeighbors]
	return removeEdges(removeQueue[0:numRemovals], capacity, neighbors)

def removeEdges(removals, preCapacity, preNeighbors):
	capacity = [row[:] for row in preCapacity]
	neighbors = [row[:] for row in preNeighbors]
	for r in removals:
		(start, end, x) = route[r]
		capacity[start][end] = 0
		capacity[end][start] = 0
		neighbors[start].remove(end)
		neighbors[end].remove(start)
	return (capacity, neighbors)

def restoreEdges(restored, preCapacity, preNeighbors):
	capacity = [row[:] for row in preCapacity]
	neighbors = [row[:] for row in preNeighbors]
	for r in restored:
		(start, end, cap) = route[r]
		capacity[start][end] = cap
		capacity[end][start] = cap
		neighbors[start].append(end)
		neighbors[end].append(start)
	return (capacity, neighbors)

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

def optimizeRailways(capacity, neighbors):
	#removedEdges = 0
	#maxFlow = findMaxFlow(capacity, neighbors)

	def binSearch(min, max, edges, flow):
		#print("In binSearch with min = " + str(min) + " & max = " + str(max))
		index = int((min+max)/2)
		(capacity, neighbors) = reducedCapacity(index)
		newMaxFlow = findMaxFlow(capacity, neighbors)
		gc.collect()

		if (newMaxFlow >= requiredFlow):
			if (min == max): return (edges, flow)
			else: return binSearch(index+1, max, index, newMaxFlow)
		else:
			if (min == max): return (edges, flow)
			return binSearch(min, index, edges, flow)

	return binSearch(1, maxRemovals, 0, findMaxFlow(capacity, neighbors))

if (numNodes >= 5): debugEnabled = True
(maxRemovals, finalMaxFlow) = optimizeRailways(initialCapacity, initialNeighbors)
print(str(maxRemovals) + " " + str(finalMaxFlow))
#printDebugs()
