import re
from cfbd.rest import ApiException

# Returns a list of the favored and unfavored teams from the chosen bet
# RETURN TYPE: list = [string, string]
def GetFavoredAndUnfavoredTeamList(betProvider, api_instance, year, week, team, conference):
    try:
        # Retrieve API response
        apiResponse = api_instance.get_lines(
            year=year, week=week, team=team, conference=conference)

        # Assign game line information to a list variable
        listOfLines = apiResponse[0].lines

        # Iterate through list of providers and their information to find user input
        for i in range(len(listOfLines)):
            # note that provider names are changed to lowercase to minimize error
            if (listOfLines[i].provider.lower() == betProvider.lower()):
                j = i

        # Create a string containing the favored team using regex and identify favored team
        favoredTeamUnedited = re.search(
            '[a-zA-Z ]*', listOfLines[j].formatted_spread).group()
        favoredTeam = favoredTeamUnedited.rstrip()

        # Identify unfavored team
        homeTeam = apiResponse[0].home_team
        if (homeTeam == favoredTeam):
            unfavoredTeam = apiResponse[0].away_team
        else:
            unfavoredTeam = apiResponse[0].home_team

        # Create a list containing the favored team as element 0 and the unfavore team as element 1
        listFavoredAndUnfavoredTeams = [favoredTeam, unfavoredTeam]

    except ApiException as e:
        print("Exception when calling BettingApi->get_lines: %s\n" % e)
    return(listFavoredAndUnfavoredTeams)

# Returns a boolean identifying if the user chose the favored team or not
# RETURN TYPE: boolean
def GetUserBetOnFavoredOrUnfavoredTeam(favoredTeam, team):
    if (favoredTeam == team):
        betOnFavoredTeam = True
    else:
        betOnFavoredTeam = False
    return(betOnFavoredTeam)

# Returns the line of the chosen point spread bet
# RETURN TYPE: floating point
def GetUserSpreadLine(betProvider, api_instance, year, week, team, conference, listFavoredAndUnfavoredTeams, betOnFavoredTeam):
    try:
        # Retrieve API response
        apiResponse = api_instance.get_lines(
            year=year, week=week, team=team, conference=conference)

        # Assign game line information to a list variable
        listOfLines = apiResponse[0].lines
        listLength = len(listOfLines)

        # Iterate through list of providers and their information to find user input
        for i in range(listLength):
            # note that provider names are changed to lowercase to minimize error
            if (listOfLines[i].provider.lower() == betProvider.lower()):
                j = i

        # Return the spread
        chosenSpread = listOfLines[j].spread
        chosenSpread = float(chosenSpread)

        # Add correct positive or negative sign to spread, because if favored team is away there is a positive sign on the spread from the api (and vice versa)
        homeTeam = apiResponse[0].home_team
        # Favored team is away, and bet is on the favored team (needs a sign flip)
        if (homeTeam == listFavoredAndUnfavoredTeams[1] and betOnFavoredTeam == True):
            chosenSpread = chosenSpread * -1
        # Favored team is home, and bet is on the unfavored team (needs a sign flip)
        elif (homeTeam == listFavoredAndUnfavoredTeams[0] and betOnFavoredTeam == False):
            chosenSpread = chosenSpread * -1

    except ApiException as e:
        print("Exception when calling BettingApi->get_lines: %s\n" % e)

    return(chosenSpread)

# Print chosen bet information when user bets on a point spread
def PrintSpreadBettingInfo(betSpreadOrLine, listFavoredAndUnfavoredTeams, chosenTeam):

    # Print user's bet information
    print("\nThe chosen spread is {}".format(betSpreadOrLine))
    print("The chosen team is {}".format(chosenTeam))
    print("Favored team: {}".format(listFavoredAndUnfavoredTeams[0]))
    print("Unfavored team: {}".format(listFavoredAndUnfavoredTeams[1]))

    return()

# Returns the game score differential information
# RETURN TYPE: list = [int, string, int, int]
def GetScoreDifferentialList(api_instance, year, week, team, conference, favoredTeam):
    try:
        # Retrieve API response
        apiResponse = api_instance.get_lines(
            year=year, week=week, team=team, conference=conference)

        # Identify score of favored team and unfavored team
        homeTeam = apiResponse[0].home_team
        if (homeTeam == favoredTeam):
            favoredTeamScore = apiResponse[0].home_score
            unfavoredTeamScore = apiResponse[0].away_score
            unfavoredTeam = apiResponse[0].away_team
        else:
            favoredTeamScore = apiResponse[0].away_score
            unfavoredTeamScore = apiResponse[0].home_score
            unfavoredTeam = apiResponse[0].home_team

        # Calculate score differential and format it
        scoreDiff = unfavoredTeamScore - favoredTeamScore
        if (scoreDiff > 0):
            formattedScoreDiff = unfavoredTeam + " is winning by {} points".format(scoreDiff)
        elif (scoreDiff == 0):
            formattedScoreDiff = "{} and {} are tied." .format(favoredTeam, unfavoredTeam)
        elif (scoreDiff < 0):
            positiveScoreDiff = scoreDiff * -1
            formattedScoreDiff = favoredTeam +  " is winning by {} points".format(positiveScoreDiff)

        # Store score differential and formatted actual spread in a list
        listScoreInfo = [int(scoreDiff), formattedScoreDiff, int(favoredTeamScore), int(unfavoredTeamScore)]

    except ApiException as e:
        print("Exception when calling BettingApi->get_lines: %s\n" % e)
    return(listScoreInfo)

# Print score information
def PrintSpreadBetCurrentScoreInfo(homeVsVistorScore, listScoreDifferential):

    print("\nCurrent Score: {}".format(homeVsVistorScore))
    print("Favored team score: {}".format(listScoreDifferential[2]))
    print("Unfavored team score: {}".format(listScoreDifferential[3]))
    print("{}".format(listScoreDifferential[1]))

    return()

# Calculate cash based on point spread bet and returns the new cash amount
# RETURN TYPE: integrer
def CalculateCashFromSpreadBet(currentCash, betAmount, betOnFavoredTeam, betSpread, scoreDiff):
    
    # Update currentCash based on bets
    if (scoreDiff < betSpread and betOnFavoredTeam == True):      # Won bet
        newCash = currentCash + int(betAmount)
    elif (scoreDiff > betSpread and betOnFavoredTeam == True):    # Lost bet
        newCash = currentCash - int(betAmount)
    elif (scoreDiff < betSpread and betOnFavoredTeam == False):   # Lost bet
        newCash = currentCash - int(betAmount)
    elif (scoreDiff > betSpread and betOnFavoredTeam == False):   # Won bet
        newCash = currentCash + int(betAmount)
    else:                                                       # Pushed bet
        newCash = currentCash
    return(newCash)
