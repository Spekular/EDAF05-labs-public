#Get number of words and queries
intArgs = list(map(int, input().split()))

#People
numNodes = intArgs[0]
#Pairs
numEdges = intArgs[1]

#Initialize list of edges
edges = []

for i in range(0, numEdges):
	edges.append(list(map(int, input().split())))

#Initialize list of nodes
nodes = set()
for edge in edges:
	nodes.add(edge[0])
	nodes.add(edge[1])

maxNode = max(nodes)
parent = [i for i in range(0, maxNode + 1)]
size = [1 for i in range(0, maxNode + 1)]

def union(start, end):
	u = find(start)
	v = find(end)
	if (size[u] < size[v]):
		parent[u] = v
		size[v] = size[u] + size[v]
	else:
		parent[v] = u
		size[u] = size[u] + size[v]

def find(node):
	v = node
	p = v
	while (parent[p] != p):
		p = parent[p]
	while (parent[v] != p):
		w = parent[v]
		parent[v] = p
		v = w
	return p

def safeEdge(start, end):
	return find(start) != find(end)

tree = []
remaining = sorted(edges, key=lambda edge: -edge[2])

while remaining:
	e = remaining.pop()
	if safeEdge(e[0], e[1]):
		union(e[0], e[1])
		#tree.append(e)
		tree.append(e[2])

print(sum(tree))
#print(sum(map(lambda edge: edge[2], tree)))
