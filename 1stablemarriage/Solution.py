import sys

class Man:
	idNum = 33333

	def __init__(self, idNum, *preferences):
		assert type(idNum) == int
		self.idNum = idNum
		self.preferences = list(preferences)
		self.proposed = -1

	def nextWoman(self):
		self.proposed += 1
		pref = list(self.preferences)
		return pref[self.proposed]

class Woman:
	def __init__(self, idNum, *preferences):
		self.idNum = idNum
		self.preferences = list(preferences)
		self.husband = -1

	def court(self, man):
		if self.husband < 0:
			self.husband = man
			return -1
		elif self.preferences.index(man) < self.preferences.index(self.husband):
			oldHusband = self.husband
			self.husband = man
			return oldHusband
		else:
			return -2

def main(inputs):
	numPairs = int(inputs[0])

	womenAdded = set()
	women = {}
	men = {}

	for index in range( 1, len(inputs), numPairs + 1):
		idNum = int(inputs[index])
		preferences = map(int, inputs[index + 1: index + 1 + numPairs])

		if idNum in womenAdded:
			men.update( {idNum: Man(idNum, *preferences)} )
		else:
			womenAdded.add(idNum)
			women.update( {idNum: Woman(idNum, *preferences)} )

	singleMen = list(men.keys())

	while singleMen:
		man = men.get(singleMen[0])
		nextWoman = man.nextWoman()
		woman = women.get(nextWoman)
		dumpedMan = woman.court(man.idNum)

		if dumpedMan != -2:
			singleMen.pop(0)
		if dumpedMan >= 0:
			singleMen.append(dumpedMan)

	for i in range(0, len(women)):
		woman = women.get(i + 1)
		print(woman.husband)

args = []
while True:
	try:
		args.extend(input().split())
	except EOFError:
		break

main(args)
