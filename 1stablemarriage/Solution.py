import sys

in1 = ["2", "1", "1", "2", "2", "2", "1", "1", "1", "2", "2", "2", "1"]

class Man:
	def __init__(self, id, *preferences):
		self.id = id
		self.preferences = preferences
		self.proposed = -1
	def __str__(self):
		return "man!"

class Woman:
	def __init__(self, id, *preferences):
		self.id = id
		self.preferences = preferences
		self.husband = -1

def main(fakeargv):
	numPairs = int(fakeargv[0])

	womenAdded = set()
	women = {}
	men = {}

	for index in range( 1, len(fakeargv), numPairs + 1):
		id = int(fakeargv[index])
		preferences = fakeargv[index + 1: index + 1 + numPairs]

		if id in womenAdded:
			men.update( {id: Man(id, preferences)} )
		else:
			womenAdded.add(id)
			women.update( {id: Woman(id, preferences)} )

	singleMen = men.keys()

main(in1)
