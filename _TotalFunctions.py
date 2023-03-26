from cfbd.rest import ApiException

# Returns a list of the user's point total bet information 
# RETURN TYPE: list = [boolean, string]
def GetUserBetOnOverOrUnder(userInputOverOrUnder):

    # Create a boolean (over = true, under = false) and a string variable based on user's input of over or under
    if (userInputOverOrUnder == "Over" or userInputOverOrUnder == "over"):
        boolBetOnOver = True
        stringOverOrUnder = "over"
    elif (userInputOverOrUnder == "Under" or userInputOverOrUnder == "under"):
        boolBetOnOver = False
        stringOverOrUnder = "under"

    listUserOverOrUnder = [boolBetOnOver, stringOverOrUnder]

    return(listUserOverOrUnder)

# Returns the line of the chosen point total bet 
# RETURN TYPE: floating point
def GetUserTotalLine(betProvider, api_instance, year, week, team, conference):
    try:
        # Retrieve API response
        apiResponse = api_instance.get_lines(year = year, week = week, team = team, conference = conference)
        
        # Assign game line information to a list variable
        listOfLines = apiResponse[0].lines
        listLength = len(listOfLines)

        # Iterate through list of providers and their information to find user input
        for i in range(listLength):
            if (listOfLines[i]['provider'].lower() == betProvider.lower()): # note that provider names are changed to lowercase to minimize error
                j = i

        # Return the spread or O/U
        betLine = listOfLines[j]['overUnder']
        betLine = float(betLine)

    except ApiException as e:
        print("Exception when calling BettingApi->get_lines: %s\n" % e)

    return(betLine)

# Returns the total score information
# RETURN TYPE: integer
def GetTotalScore(api_instance, year, week, team, conference):
    try:
        # Retrieve API response
        apiResponse = api_instance.get_lines(year = year, week = week, team = team, conference = conference)

        # Identify score of favored team and unfavored team
        homeTeamScore = apiResponse[0].home_score
        awayTeamScore = apiResponse[0].away_score

        # Calculate total score
        totalScore = homeTeamScore + awayTeamScore
        totalScore = int(totalScore)

    except ApiException as e:
        print("Exception when calling BettingApi->get_lines: %s\n" % e)
    return(totalScore)

# Print score information
def PrintTotalBetCurrentScoreInfo(homeVsVistorScore,totalScore):

    print("\nCurrent Score: {}".format(homeVsVistorScore))
    print("Total Score: {}".format(totalScore))

    return()

# Calculate cash based on point total O/U bet
# RETURN TYPE: integer
def CalculateCashFromTotalBet(currentCash, betAmount, betLine, betOnOver, actualTotalScore):
    # Update currentCash based on bets
    if (betLine < actualTotalScore and betOnOver == True):      # Won bet
        newCash = currentCash + int(betAmount)
    elif (betLine > actualTotalScore and betOnOver == True):    # Lost bet
        newCash = currentCash - int(betAmount)
    elif (betLine < actualTotalScore and betOnOver == False):   # Lost bet
        newCash = currentCash - int(betAmount)
    elif (betLine > actualTotalScore and betOnOver == False):   # Won bet
        newCash = currentCash + int(betAmount)
    else:                                                       # Pushed bet
        newCash = currentCash
    return(newCash)