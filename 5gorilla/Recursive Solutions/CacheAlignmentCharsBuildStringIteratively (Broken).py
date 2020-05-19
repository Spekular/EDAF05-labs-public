import sys

sys.setrecursionlimit(10**5)

#Get valid letter
alphabet = list(input().split())
numChars = len(alphabet)

charToIndex = {i:alphabet[i] for i in range(0, numChars)}

costs = []
for i in range(0, numChars):
	costs.append(list(map(int, input().split())))

matchScore = {}
for i in range(0, numChars):
	for j in range(0, numChars):
		matchScore[(alphabet[i], alphabet[j])] = costs[i][j]

numQueries = int(input())

queries = []
for i in range(0, numQueries):
	queries.append(input().split())

#This will store completed alignments
alignments = []

#Dictionary used in initial implementation. By using the string pair as a key,
#the dictionary could be sed by any pair of strings,
#optimalAlignment = {
#	("", "") : (0, "", "")
#}

#Align two strings with caching exclusive to the pair
def align(initialTop, initialBot):
	topLen = len(initialTop)
	botLen = len(initialBot)
	alignmentCached = [[0 for j in range(botLen + 1)] for i in range(topLen + 1)]
	cachedAlignment = [[(0, 0, 0, "", "") for j in range(botLen + 1)] for i in range(topLen + 1)]
	alignmentCached[topLen][botLen] = 1

	def optAlign(topDrop, top, botDrop, bot):
		if (topDrop == topLen and botDrop == botLen):
			return (0, "", "")
		elif alignmentCached[topDrop][botDrop] != 0:
			topDropped = topDrop
			botDropped = botDrop
			topChars = []
			botChars = []
			score = cachedAlignment[topDropped][botDropped][0]
			while (topDropped != topLen) or (botDropped != botLen):
				(score, td, bd, thisTop, thisBot) = cachedAlignment[topDropped][botDropped]
				topChars.append(thisTop)
				botChars.append(thisBot)
				topDropped = topDropped + td
				botDropped = botDropped + bd
			return (score, ''.join(topChars), ''.join(botChars))
		else:
			result = (0, "", "")
			td = -1
			bd = -1

			if (top == ""):
				td = 0
				bd = botLen - botDrop
				result = (bd * -4, "*" * bd, bot)
			elif (bot == ""):
				td = topLen - topDrop
				bd = 0
				result = (td * -4, top, "*" * td)
			else:
				both = keepBoth(topDrop, top, botDrop, bot)
				insTop = insertTop(topDrop, top, botDrop, bot)
				insBot = insertBot(topDrop, top, botDrop, bot)

				if (both[0] > insTop[0] and both[0] > insBot[0]):
			 		result = both
			 		td = 1
			 		bd = 1
				elif (insTop[0] > insBot[0]):
			 		result = insTop
			 		td = 0
			 		bd = 1
				else:
			 		result = insBot
			 		td = 1
			 		bd = 0

			score = result[0]
			thisTop = result[1][:1]
			thisBot = result[2][:1]

			cachedAlignment[topDrop][botDrop] = (score, td, bd, thisTop, thisBot)
			alignmentCached[topDrop][botDrop] = 1

			return result

	def keepBoth(topDrop, top, botDrop, bot):
		(rScore, rTop, rBot) = optAlign(topDrop + 1, top[1:], botDrop + 1, bot[1:])
		score = matchScore[(top[0],bot[0])]
		return (rScore + score, top[0] + rTop, bot[0] + rBot)

	def insertTop(topDrop, top, botDrop, bot):
		(rScore, rTop, rBot) = optAlign(topDrop, top, botDrop + 1, bot[1:])
		score = -4
		return (rScore + score, "*" + rTop, bot[0] + rBot)

	def insertBot(topDrop, top, botDrop, bot):
		(rScore, rTop, rBot) = optAlign(topDrop + 1, top[1:], botDrop, bot)
		score = -4
		return (rScore + score, top[0] + rTop, "*" + rBot)

	return optAlign(0, initialTop, 0, initialBot)

#Find alignments for all queries
for i in range(0, numQueries):
	query = queries[i]
	(score, top, bot) = align(query[0], query[1])
	alignments.append(top + " " + bot)

#Print alignments for all queries
for alignment in alignments: print(alignment)
