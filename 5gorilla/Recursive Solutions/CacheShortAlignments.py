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
def align(initialTop, initialBot):
	topLen = len(initialTop)
	botLen = len(initialBot)
	alignmentCached = [[0 for j in range(botLen + 1)] for i in range(topLen + 1)]
	cachedAlignment = [[(0, "", "") for j in range(botLen + 1)] for i in range(topLen + 1)]
	alignmentCached[topLen][botLen] = 1

	def optAlign(topDrop, top, botDrop, bot):
		if alignmentCached[topDrop][botDrop] != 0:
			return cachedAlignment[topDrop][botDrop]
		else:
			result = (0, "", "")
			if (top == ""):
				remaining = botLen - botDrop
				result = (remaining * -4, "*" * remaining, bot)
			elif (bot == ""):
				remaining = topLen - topDrop
				result = (remaining * -4, top, "*" * remaining)
			else:
				result = keepBoth(topDrop, top, botDrop, bot)
				insTop = insertTop(topDrop, top, botDrop, bot)
				insBot = insertBot(topDrop, top, botDrop, bot)

				if (insTop[0] > result[0]): result = insTop
				if (insBot[0] > result[0]): result = insBot


			cache = (topLen-topDrop) <= 1800 and (botLen-botDrop) <= 1800
			if (cache):
				cachedAlignment[topDrop][botDrop] = result
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
