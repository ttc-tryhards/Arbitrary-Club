from enum import Enum

class Games(Enum):
    mainGame = 0
    mindBender = 1
    e60 = 2
    nblox = 3

class SortModes(Enum):
    alpha = 0
    tier = 1

class Player:
    sortMode = SortModes.alpha
    def __init__(self, name):
        self.name = name
        self.scores = dict()
        self.scores[Games.mainGame] = 0
        self.scores[Games.mindBender] = 0
        self.scores[Games.e60] = 0
        self.scores[Games.nblox] = 0

        self.tier = 0
        self.nextTierProgress = "0/4"
        self.tierPlus = "0 0/4"
    
    def getScores(self):
        ans = ""
        for key in self.scores.keys():
            ans += str(key) + ": "
            ans += str(self.scores[key]) +"\n"
        return ans[:-1]

    def setTiers(self):
        self.tier = getPlayerTier(self.name)
        self.nextTierProgress = getPlayerTierCompletion(self.name, self.tier + 1)
        self.tierPlus = getPlayerTierPlus(self.name)

    def getTierCompletionCSVString(self, tier):
        ans = self.name + ","
        for game in Games:
            if self.scores[game] >= tiers[game][tier]:
                ans += "✓,"
            else:
                ans += "X,"
        return ans

    def __lt__(self, other):
        operand1 = ""
        operand2 = ""
        match Player.sortMode:
            case SortModes.alpha:
                return self.name.lower() < other.name.lower()
            case SortModes.tier:
                #sorts with larger tiers on top
                if self.tier == other.tier:
                    return self.nextTierProgress >= other.nextTierProgress
                else:
                    return self.tier >= other.tier
            case Games.mainGame:
                return self.scores[Games.mainGame] < other.scores[Games.mainGame]
            case Games.mindBender:
                return self.scores[Games.mindBender] < other.scores[Games.mindBender]
            case Games.e60:
                return self.scores[Games.e60] < other.scores[Games.e60]
            case Games.nblox:
                return self.scores[Games.nblox] < other.scores[Games.nblox]

    def __eq__(self, other):
        if type(other) == type(self):
            return self.name == other.name
        elif type(other) == type("a"):
            return self.name == other

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
    
#reads a tsv to a 2d array
def readCSV(filename, delimiter = "\t"):
    with open(filename, encoding="utf8") as f:
        rawText = f.read()
    lines = rawText.split("\n")
    for i in range(len(lines)):
        lines[i] = lines[i].split(delimiter)
    return lines

def writeCSV(filename, delimiter = ","):
    pass

def joinCSV(list):
    for i in range(len(list)):
        list[i] = list[i].split("\n")
    
    ans = ""
    for i in range(len(list[0])):
        ans += ",".join([list[j][i] for j in range(len(list))]) + "\n"
    return ans

def readLeaderboard(filename, game):
    def findPoints(values):
        for i in range(len(values)):
            for j in range(len(values[i])):
                if values[i][j].lower() == "points" or values[i][j].lower() == "points (level 1 start)":
                    yield (i+2, j)
    
    def readLocation(i, j):
        name, score = values[i][j], readNumber(values[i][j+1])
        while True:
            name = values[i][j]
            if name == "":
                break
            score = readNumber(values[i][j+1])
            i+=1
            #if player is in the dictionary update their score, else add them to the dict
            if name in players:
                if players[name].scores[game] < score:
                    players[name].scores[game] = score
            else:
                players[name] = Player(name)
                players[name].scores[game] = score
    
    values = readCSV(filename)
    for i, j in findPoints(values):
        readLocation(i, j)

#designed to read numbers in text format to integer format ie. "1.5m" -> 1,500,000
def readNumber(num):
    if num == "B125B":
        return num
    #removes commas
    for i in range(len(num) - 1, -1, -1):
        if num[i] == ",":
            num = num[0:i] + num[i+1:]
    
    suffix = ""
    if num[-1:].isalpha():
        suffix = num[-1].lower()
        num = num[:-1]
    
    ans = float(num)
    if suffix == "m":
        ans *= 1000000
    if suffix == "k":
        ans *= 1000
    return int(ans)

#returns a dict where each score threshold can be accessed by format dict[gamename][tiernumber]
def readTiers():
    values = readCSV(r'.\_Arbitrary Club_ Tiers - Tiers.csv', ",")
    tierMap = dict()
    burn = [game for game in Games]
    for i in range(len(values)):
        key = burn[i]
        tierMap[key] = dict()
        for j in range(1,len(values[i])):
            tierMap[key][j] = readNumber(values[i][j])
    return tierMap

#returns player tier (ie: 4)
def getPlayerTier(playerName):
    player = players[playerName]

    for tier in range(1,6):
        for game in Games:
            if player.scores[game] < tiers[game][tier]:
                player.tier = tier - 1
                return tier - 1

#return completion of a tier out of 4 (ie: 2/4)
def getPlayerTierCompletion(playerName, tier):
    ans = 0
    player = players[playerName]
    for game in Games:
        if player.scores[game] >= tiers[game][tier]:
                ans += 1
    return str(ans) + "/4"

#returns players tier plus completion of the next tier up (ie: 3 3/4)
def getPlayerTierPlus(playerName):
    tier = getPlayerTier(playerName)
    tierCompletion = getPlayerTierCompletion(playerName, tier+1)
    return str(tier) + " " + tierCompletion

#globals
players = dict()
tiers = readTiers()

def printCaseSensitiveNameCheck(playerList):
    Player.sortMode = SortModes.alpha
    playerList.sort()
    #case-check
    flag = True
    for i in range(len(playerList)-1):
        if playerList[i].name.lower() == playerList[i+1].name.lower():
            if flag:
                print("THESE PLAYERS HAVE NAMES THAT ARENT CASE MATCHING (ie Goldenrod and goldenrod)")
                flag = False
            print(playerList[i].name, playerList[i+1].name)
    if flag:
        print("No non-case-matching names found.")

def outputTierLeaderboard(playerList):
    #prints top players by tier
    Player.sortMode = SortModes.tier
    playerList.sort()

    place = 0
    frozenPlace = 0 #deals with ties
    output = ["Place,Name,Tier"]
    for playerIndex in range(len(playerList)):
        player = playerList[playerIndex]
        place += 1
        if player.tierPlus != playerList[playerIndex-1].tierPlus:
            frozenPlace = place

        output.append(str(frozenPlace) + "," + player.name + "," + player.tierPlus)
    
    with open(r'tiersLeaderboard.csv', mode="w", encoding="utf8") as f:
        f.write("\n".join(output))
    
    



def main():
    #reads from all leaderboards
    readLeaderboard(r'.\Tetris.com high scores - Tetris.tsv', Games.mainGame)
    readLeaderboard(r'.\Tetris.com high scores - Mind Bender.tsv', Games.mindBender)
    readLeaderboard(r'.\Tetris.com high scores - N-Blox.tsv', Games.nblox)
    readLeaderboard(r'.\Tetris.com high scores - e60.tsv', Games.e60)

    #defines a list of players
    playerList = []
    for player in players.values():
        player.setTiers()
        playerList.append(player)
    
    #performs case check, so that Goldenrod, and goldenrod cant be two distinct people - PLAYERS OUTPUT BY THIS SHOULD BE MANUALLY FIXED ON THE LBS
    printCaseSensitiveNameCheck(playerList)
    outputTierLeaderboard(playerList)

    
    totalOutput = []
    for i in range(1,6):
        output = "Tier " + str(i) + " Completion,,,,,\n" + ",Main Game, Mind Bender, e60, nblox,\n"
        lineCount = 1
        for player in playerList:
            if getPlayerTierCompletion(player.name, i) != "0/4":
                lineCount+=1
                output += player.getTierCompletionCSVString(i) + "\n"
        
        #pads all tiers to same length with blank fields
        while lineCount < 200:
            output += ",,,,\n"
            lineCount += 1
        totalOutput.append(output)
    
    with open(r'output.csv', mode="w", encoding="utf8") as f:
        f.write(joinCSV(totalOutput))

    
main()