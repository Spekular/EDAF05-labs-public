import math

#Get number of points
numPoints = int(input())

#Get point coordinates
rawPoints = []

for i in range(0, numPoints):
	rawPoints.append(list(map(int, input().split())))

pointsByX = sorted(rawPoints, key=lambda p: p[0])
pointsByY = sorted(rawPoints, key=lambda p: p[1])

#Unnecessarily many helper functions
#def vectorLength(vector):
#	return math.sqrt(vector[0]**2 + vector[1]**2)

#def pointDelta(a, b):
#	return [a[0] - b[0], a[1] - b[1]]

def pointDistance(a, b):
	return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
	#return vectorLength(pointDelta(a,b))

#Naive closest function (we use it for 3 or fewer points)
def closestNaive(points):
	distance = pointDistance(points[0], points[1])
	for i in range (2, len(points)):
		candidate = pointDistance(points[i - 1], points[i])
		if candidate < distance: distance = candidate
	return distance

#Return (lx, rx, ly, ry). We iteratively populate these lists in order to:
# - keep ly and ry stable (avoid re-sorting by y)
# - ensure that points with the same x coord never end up on different sides
def recArgs(px, py, n):
	midpoint = px[int(n/2)-1]
	middleX = midpoint[0]

	lx = []
	rx = []
	ly = []
	ry = []

	#for i in range (0, n):
	#	if px[i][0] <= middleX:
	#		lx.append(px[i])
	#	else: rx.append(px[i])
	#	if py[i][0] <= middleX:
	#		ly.append(py[i])
	#	else: ry.append(py[i])

	lx = px[:int(n/2)]
	rx = px[int(n/2):]
	ly = sorted(lx, key=lambda p: p[1])
	ry = sorted(rx, key=lambda p: p[1])

	return (lx, rx, ly, ry)


def closest (px, py, n):
	if n == 1: return (2 * 10**9)
	if n <= 3: return closestNaive(px)
	#Returns (lx, rx, ly, ry)
	args = recArgs(px, py, n)
	leftDelta = closest(args[0], args[2], len(args[0]))
	rightDelta = closest(args[1], args[3], len(args[1]))
	delta = leftDelta if (leftDelta < rightDelta) else rightDelta
	middleX = args[0][-1][0]

	nearMiddle = []
	for point in py:
		x = point[0]
		if x >= (middleX - delta) and x <= (middleX + delta):
			nearMiddle.append(point)

	numNearMiddle = len(nearMiddle)
	for i in range (0, numNearMiddle):
		for j in range(i + 1, min(i + 15, numNearMiddle - 1)):
			candidate = pointDistance(nearMiddle[i], nearMiddle[j])
			delta = candidate if (candidate < delta) else delta

	return delta

shortestDistance = closest(pointsByX, pointsByY, numPoints)
print("{:1.6f}".format(shortestDistance))
