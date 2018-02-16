import json
import radarPlot
import spreadsheetMaker

class Match(object):

    def __init__(self,number,red,blue,random):
        self.dict = {"number": number,"red": red,"blue": blue,"random": random}
        
    def returnMatch(self):
        returnStr = ""
        for key in self.dict:
            returnStr += key + ": " + (str)(self.dict[key]) + "\n"
        return returnStr

    def importDict(self,diction):
        for key in self.dict:
            self.dict[key] = diction[key]

class Team(object):

    def __init__(self,teamNum):
        self.dict =  {"matches": [],"number": teamNum,"autoPenalty": [],"autoLine": [],"autoSwitch": [],"autoScale": [],
                      "startingPos": [],"teleSwitch": [],"teleOppSwitch": [],"teleScale": [],"hang": [],
                      "assistance": [],"vaultBlocks": [],"comments": [],"cims": 0,"wheels": 0,"drivetrain": "",
                      "weight": 0,"preAuto": "","preTele": "","preHang": "","preAssist": ""}

    def returnTeam(self):
        returnStr = ""
        for key in self.dict:
            returnStr += key + ": " + (str)(self.dict[key]) + "\n"
        return returnStr

    def addMatch(self,matchNum,general,scale,comment):
        self.dict["matches"].append((int)(matchNum))
        self.dict["autoPenalty"].append(general[0])
        self.dict["autoLine"].append(general[1])
        self.dict["autoSwitch"].append(general[2])
        self.dict["autoScale"].append(general[3])
        self.dict["startingPos"].append(general[4])
        self.dict["teleSwitch"].append(general[5])
        self.dict["teleOppSwitch"].append(general[6])
        self.dict["teleScale"].append(scale)
        self.dict["hang"].append(general[7])
        self.dict["assistance"].append(general[8])
        self.dict["vaultBlocks"].append(general[9])
        self.dict["comments"].append(comment)

    def addPreData(self,preData):
        self.dict["cims"] = preData[1]
        self.dict["wheels"] = preData[2]
        self.dict["drivetrain"] = preData[3]
        self.dict["weight"] = preData[4]
        self.dict["preAuto"] = preData[5]
        self.dict["preTele"] = preData[6]
        self.dict["preHang"] = preData[7]
        self.dict["preAssist"] = preData[8]

    def importDict(self,diction):
        for key in self.dict:
            self.dict[key] = diction[key]

def enterMatch():
    matchInfo = raw_input("Enter match string: ").split()
    
    number = matchInfo[0]
    red = []
    blue = []
    random = []
    for num in range(1,4):
        red.append((str)(matchInfo[num])) 
    for num in range(4,7):
        blue.append((str)(matchInfo[num])) 
    for num in range(7,9):
        random.append(matchInfo[num])
    match = Match(number,red,blue,random)
    matchList.append(match)
    return match

def makeSpreadsheet():
    spreadsheetMaker.makeSpreadsheet()

def createRadarPlot(team):
    teamNum = team.dict["number"]
    numMatches = (float)(len(team.dict["matches"]))
    if(numMatches == 0):
        numMatches = 1
    
    agility = 0
    if((int)(team.dict["cims"]) >= 6 and (int)(team.dict["weight"]) <= 100):
        agility = 5
    elif((int)(team.dict["cims"]) >= 6 and (int)(team.dict["weight"]) > 100):
        agility = 4
    elif((int)(team.dict["cims"]) >= 4 and (int)(team.dict["weight"]) <= 100):
        agility = 3
    elif((int)(team.dict["cims"]) >= 4 and (int)(team.dict["weight"]) > 100):
        agility = 2
    elif((int)(team.dict["cims"]) >= 2 and (int)(team.dict["weight"]) <= 100):
        agility = 1
        
    switch = 0
    sumSwitch = 0
    for i in range(0,len(team.dict["matches"])):
        cubes = team.dict["teleSwitch"][i] + team.dict["teleOppSwitch"][i]
        if(cubes >= 7):
            sumSwitch += 5
        elif(cubes >= 5):
            sumSwitch += 4
        elif(cubes >= 3):
            sumSwitch += 3
        elif(cubes >= 2):
            sumSwitch += 2
        elif(cubes > 0):
            sumSwitch += 1
    switch = (float)(sumSwitch)/numMatches
    
    scale = 0
    sumScale = 0
    for i in range(0,len(team.dict["matches"])):
        cubes = 0
        acc = 0
        for delivery in team.dict["teleScale"][i]:
            if((int)(delivery[1]) == 1):
                cubes += 1
            acc += 1
        acc = (float)(cubes)/(float)(acc)
        if(acc <= 0.25 and cubes > 0):
            sumScale += 1
        elif(cubes >= 7 and acc >= 0.75):
            sumScale += 5
        elif((cubes >= 5 and acc >= .75) or cubes >= 7):
            sumScale += 4
        elif((cubes >= 3 and acc >= .75) or cubes >= 5):
            sumScale += 3
        elif((cubes > 0 and acc >= .75) or cubes >= 3):
            sumScale += 2
        elif(cubes >= 3):
            sumScale += 1
    scale = (float)(sumScale)/numMatches
    
    hang = 0
    sumHang = 0
    for i in range(0,len(team.dict["matches"])):
        result = (int)(team.dict["hang"][i])
        if(result == 0):
            sumHang += 1
        elif(result == -1):
            sumHang += 0
        elif(result > 30):
            sumHang += 1
        elif(result > 25):
            sumHang += 2
        elif(result > 20):
            sumHang += 3
        elif(result > 15):
            sumHang += 4
        elif(result < 15):
            sumHang += 5
    hang = (float)(sumHang)/numMatches
    
    assist = 0
    sumAssist = 0
    for i in range(0,len(team.dict["matches"])):
        result = (int)(team.dict["assistance"][i])
        if(result == 0):
            sumAssist += 3
        elif(result == -1):
            sumAssist += 0
        elif(result == 1):
            sumAssist += 5
    assist = (float)(sumAssist)/numMatches
    
    auto = 0
    sumAuto = 0
    for i in range(0,len(team.dict["matches"])):
        line = (int)(team.dict["autoLine"][i])
        switch = (int)(team.dict["autoSwitch"][i])
        scale = (int)(team.dict["autoScale"][i])
        penalty = (int)(team.dict["autoPenalty"][i])
        if(penalty == 1):
            sumAuto -= 1
        elif(line == 1 and switch > 1 and scale > 1):
            sumAuto += 5
        elif(line == 1 and (switch > 1 or scale > 1)):
            sumAuto += 4
        elif(line == 1 and scale > 0):
            sumAuto += 3
        elif(line == 1 and switch > 0):
            sumAuto += 2
        elif(line == 1):
            sumAuto += 1
    auto = (float)(sumAuto)/numMatches
    if(auto < 0):
        auto = 0

    print agility,switch,scale,hang,assist,auto
    radarPlot.createRadarPlot(teamNum,agility,switch,scale,hang,assist,auto)
    

def enterPreData():
    tempList = []
    tempList.append(raw_input("Enter team number: "))
    tempList.append(raw_input("Enter " + tempList[0] + "'s #cims: "))
    tempList.append(raw_input("Enter " + tempList[0] + "'s #wheels: "))
    tempList.append(raw_input("Enter " + tempList[0] + "'s drivetrain: "))
    tempList.append(raw_input("Enter " + tempList[0] + "'s weight: "))
    tempList.append(raw_input("Enter " + tempList[0] + "'s auto capabilities: "))
    tempList.append(raw_input("Enter " + tempList[0] + "'s tele capabilities: "))
    tempList.append(raw_input("Enter " + tempList[0] + "'s hang capabilities: "))
    tempList.append(raw_input("Enter " + tempList[0] + "'s assist capabilities: "))
    found = False
    for team in teamList:
        if(team.dict["number"] == tempList[0]):
            team.addPreData(tempList)
            found = True
    if(not found):
        newTeam = Team(tempList[0])
        newTeam.addPreData(tempList)
        teamList.append(newTeam)
    

def enterTeams(match):
    for team in match.dict["red"]:
        enterTeam(match.dict["number"],team)
    for team in match.dict["blue"]:
        enterTeam(match.dict["number"],team)
        
def enterTeam(matchNum,teamNum):
    autoStats = []
    #tempScale = []
    scaleStats = []
    genStats = []
    userInput = []
    while(len(userInput) != 3):
        userInput = raw_input("Enter team " + (str)(teamNum) +"'s string for match #" + (str)(matchNum) + ": ").split('|')
    genStats = userInput[0].split()
    #tempScale = userInput[1].split()
    for i in range(0,len(userInput[1].split()),2):
        scaleStats.append([userInput[1].split()[i],userInput[1].split()[i+1]])
    found = False
    comment = userInput[2][1:]
    for team in teamList:
        if(team.dict["number"] == teamNum):
            team.addMatch(matchNum,genStats,scaleStats,comment)
            found = True
    if(not found):
        newTeam = Team(teamNum)
        newTeam.addMatch(matchNum,genStats,scaleStats,comment)
        teamList.append(newTeam)
    found = False

def loadMatchesList(fileName):
    matchesStr = ""
    tempList = []
    returnList = []
    matchesFile = open(fileName,'r')
    for line in matchesFile:
        matchesStr += line
    if(len(matchesStr) > 0):
        tempList = json.loads(matchesStr)
    for matchDict in tempList:
        newMatch = Match(-1,[],[],[])
        newMatch.importDict(matchDict)
        returnList.append(newMatch)
    return returnList

def loadTeamsList(fileName):
    teamsStr = ""
    tempList = []
    returnList = []
    teamsFile = open(fileName,'r')
    for line in teamsFile:
        teamsStr += line
    if(len(teamsStr) > 0):
        tempList = json.loads(teamsStr)
    for teamDict in tempList:
        newTeam = Team(-1)
        newTeam.importDict(teamDict)
        returnList.append(newTeam)
    return returnList

def save():
    teamDictList = []
    matchDictList = []
    with open('teams.txt','w') as outfile:
        for team in teamList:
            teamDictList.append(team.dict)
        json.dump(teamDictList,outfile)
    with open('matches.txt','w') as outfile:
        for match in matchList:
            matchDictList.append(match.dict)
        json.dump(matchDictList,outfile)

def commands(cmd):
    cmdarray = cmd.split()
    if(len(cmdarray) > 0):
        basecmd = cmdarray[0]
        if(basecmd == "matchReport"):
            print "Beginning Match Report"
            print ""
            print ""
            print ""
            enterTeams(enterMatch())
        elif(basecmd == "preScouting"):
            if(len(cmdarray) == 2):
                if((int)(cmdarray[1]) > 0):
                    for num in range(0,(int)(cmdarray[1])):
                        enterPreData()
                else:
                    print "Number of teams must be greater than 0."
            else:
                print "preScouting takes exactly one parameter (numberOfTeamsEntering)"
        elif(basecmd == "help"):
            print "The available commands are:",
            for cmd in cmds:
                print cmd,
            print ""
        elif(basecmd == "save"):
            print "matches.txt saved."
            print "teams.txt saved."
        elif(basecmd == "team"):
            if(len(cmdarray) == 2):
                found = False
                for team in teamList:
                    if(team.dict["number"] == cmdarray[1]):
                        found = True
                        print team.returnTeam()
                if(cmdarray[1] == "all"):
                    for team in teamList:
                        print team.returnTeam()
                    found = True
                if(not found):
                    print "Could not find team " + cmdarray[1] + "."
            else:
                print "team takes exactly one parameter (teamName)"
        elif(basecmd == "match"):
            if(len(cmdarray) == 2):
                found = False
                for match in matchList:
                    if(match.dict["number"] == cmdarray[1]):
                        found = True
                        print match.returnMatch()
                if(not found):
                    print "Could not find match #" + cmdarray[1] + "."
            else:
                print "match takes exactly one parameter (matchNumber)"
        elif(basecmd == "editTeam"):
            for team in teamList:
                if(team.dict["number"] == cmdarray[1]):
                    if(len(cmdarray) == 5):
                        if(len(team.dict[cmdarray[2]]) == 0):
                            team.dict[cmdarray[2]].append(cmdarray[4])
                        else:
                            team.dict[cmdarray[2]][cmdarray[3]] == cmdarray[4]
                    else:
                        team.dict[cmdarray[2]] = cmdarray[3]
        elif(basecmd == "radarPlot"):
            for team in teamList:
                createRadarPlot(team)
                print (str)(team.dict["number"]) + ".png created."
        elif(basecmd == "makeSpreadsheet"):
            makeSpreadsheet()
        else:
            print "Unknown command. Type 'help' for a list of valid commands."
        
    

matchList = loadMatchesList("matches.txt")
teamList = loadTeamsList("teams.txt")

cmds = ["matchReport","preScouting","team","match","help","save"]
while True:
    print "Enter a command."
    cmd = raw_input("")
    if (cmd == "devClose"):
        break
    print ""
    save()
    if (cmd == "close"):
        break
    commands(cmd)
    print ""
    



