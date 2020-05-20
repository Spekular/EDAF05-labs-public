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

#Align two strings with caching exclusive to the pair
def getScores(initialTop, initialBot):
	topLen = len(initialTop)
	botLen = len(initialBot)
	scoreCached = [[0 for j in range(botLen + 1)] for i in range(topLen + 1)]
	cachedScore = [[0 for j in range(botLen + 1)] for i in range(topLen + 1)]
	scoreCached[topLen][botLen] = 1

	def optScore(topDrop, top, botDrop, bot):
		if scoreCached[topDrop][botDrop] > 0:
			return cachedScore[topDrop][botDrop]
		else:
			if (top == ""):
				result = insertTop(topDrop, top, botDrop, bot)
			elif (bot == ""):
				result = insertBot(topDrop, top, botDrop, bot)
			else:
				result = max(
					keepBoth(topDrop, top, botDrop, bot),
					insertTop(topDrop, top, botDrop, bot),
					insertBot(topDrop, top, botDrop, bot)
				)

			cachedScore[topDrop][botDrop] = result
			scoreCached[topDrop][botDrop] = 1

			return result

	def keepBoth(topDrop, top, botDrop, bot):
		match = matchScore[(top[0],bot[0])]
		return optScore(topDrop + 1, top[1:], botDrop + 1, bot[1:]) + match

	def insertTop(topDrop, top, botDrop, bot):
		return optScore(topDrop, top, botDrop + 1, bot[1:]) - 4

	def insertBot(topDrop, top, botDrop, bot):
		return optScore(topDrop + 1, top[1:], botDrop, bot) - 4

	optScore(0, initialTop, 0, initialBot)
	return cachedScore

def align(top, bot):
	scores = getScores(top, bot)

	topLen = len(top)
	botLen = len(bot)
	iTop = 0
	iBot = 0
	topString = []
	botString = []

	while iTop < topLen and iBot < botLen:
		dropBoth = scores[iTop+1][iBot+1] + matchScore[(top[iTop],bot[iBot])]
		dropTop = scores[iTop+1][iBot] - 4
		dropBot = scores[iTop][iBot+1] - 4

		if ((dropBoth > dropTop) and (dropBoth > dropBot)):
			topString.append(top[iTop])
			botString.append(bot[iBot])
			iTop += 1
			iBot += 1
		elif (dropTop > dropBot):
			topString.append(top[iTop])
			botString.append("*")
			iTop += 1
		else:
			topString.append("*")
			botString.append(bot[iBot])
			iBot += 1

	return (scores[0][0], ''.join(topString), ''.join(botString))

#Find alignments for all queries
for i in range(0, numQueries):
	query = queries[i]
	(score, top, bot) = align(query[0], query[1])
	alignments.append(top + " " + bot)

#Print alignments for all queries
for alignment in alignments: print(alignment)
