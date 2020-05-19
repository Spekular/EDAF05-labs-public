import sys

sys.setrecursionlimit(10**6)

#Get valid letters
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

#Dictionary with optimal alignments, pre-initialized to handle two empty strings
optimalAlignment = {
	("", "") : (0, "", "")
}

def optAlign(top, bot):
	if (top, bot) in optimalAlignment:
		return optimalAlignment[(top, bot)]
	else:
		result = (0, "", "")
		if (len(top) == 0):
			remaining = len(bot)
			result = (remaining * -4, "*" * remaining, bot)
			#result = insertTop(top, bot)
		elif (len(bot) == 0):
			remaining = len(top)
			result = (remaining * -4, top, "*" * remaining)
			#result = insertBot(top, bot)
		else:
			#both = keepBoth(top, bot)
			both = optAlign(top[1:], bot[1:])
			bothScore = matchScore[(top[0],bot[0])]
			both = (both[0] + bothScore, top[0] + both[1], bot[0] + both[2])
			insTop = insertTop(top, bot)
			insBot = insertBot(top, bot)
			result = both
			if (insTop[0] > result[0]): result = insTop
			if (insBot[0] > result[0]): result = insBot

		optimalAlignment[(top, bot)] = result
		return result

def keepBoth(top, bot):
	(rScore, rTop, rBot) = optAlign(top[1:], bot[1:])
	score = matchScore[(top[0],bot[0])]
	return (rScore + score, top[0] + rTop, bot[0] + rBot)

def insertTop(top, bot):
	(rScore, rTop, rBot) = optAlign(top, bot[1:])
	score = -4
	return (rScore + score, "*" + rTop, bot[0] + rBot)

def insertBot(top, bot):
	(rScore, rTop, rBot) = optAlign(top[1:], bot)
	score = -4
	return (rScore + score, top[0] + rTop, "*" + rBot)
	#(rScore, rBot, rTop) = insertTop(bot, top)
	#return (rScore, rTop, rBot)


for i in range(0, numQueries):
	query = queries[i]
	(score, top, bot) = optAlign(query[0], query[1])
	alignments.append(top + " " + bot)

for alignment in alignments: print(alignment)

#Debug
#print(charToIndex)
#print("Alphabet:")
#print(alphabet)
#print("numChars:")
#print(numChars)
#print("numQueries:")
#print(numQueries)
#print("First query:")
#print(queries[0])
#print(costs)
