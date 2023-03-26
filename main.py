# Import core functions from other .py files in this package 
from _PrintFunctions import *
from _SpreadFunctions import *
from _TotalFunctions import *
from _CatchAllFunctions import *
from _CreateAPIInstance import *

def main():

    # Configure API key authorization and create an instance of the API class
    betting_api_instance = GetAPIInstance()

    # Print user information
    userFirstName = "John"
    userLastName = "Smith"
    userCurrentCash = 3000
    print("\nGambler's name: {} {}\nGambler's current cash: ${}\n".format(userFirstName, userLastName, userCurrentCash))
    
    # Input game information
    year = 2021 
    conference = input('Enter the conference name:\n')
    week = int(input('\nEnter the week:\n'))
    
    # Print betting information to console    
    PrintAllGamesBettingData(betting_api_instance, year, week, conference)

    # Choose team, line provider, spread or over/under, and amount to bet
    chosenTeam = input("\nEnter the team you would like to bet on\n")
    betProvider = input("\nEnter the name of your bet provider\n")
    betType = input("\nSpread or O/U?\n")
    userBetAmount = input("\nHow many dollars would you like to bet?\n")

    # If user chooses a point spread bet
    if (betType == "Spread" or betType == "spread"):

        # Get the favored team and chosen spread
        listFavoredAndUnfavoredTeams = GetFavoredAndUnfavoredTeamList(betProvider, betting_api_instance, year, week, chosenTeam, conference)
        betOnFavoredTeam =  GetUserBetOnFavoredOrUnfavoredTeam(listFavoredAndUnfavoredTeams[0], chosenTeam)
        betLine = GetUserSpreadLine(betProvider, betting_api_instance, year, week, chosenTeam, conference, listFavoredAndUnfavoredTeams, betOnFavoredTeam)

        # Print chosen bet information
        PrintSpreadBettingInfo(betLine, listFavoredAndUnfavoredTeams, chosenTeam)

        # Get current score (home vs. vistor) and score differential
        homeVsVistorScore = GetHomeVsVisitorScore(betting_api_instance, year, week, chosenTeam, conference)
        listScoreDifferential = GetScoreDifferentialList(betting_api_instance, year, week, chosenTeam, conference, listFavoredAndUnfavoredTeams[0])

        # Print score information
        PrintSpreadBetCurrentScoreInfo(homeVsVistorScore,listScoreDifferential)

        # Calculate current cash
        userNewCash = CalculateCashFromSpreadBet(userCurrentCash, userBetAmount, betOnFavoredTeam, betLine, listScoreDifferential[0])

    # If user chooses a point total O/U bet
    elif (betType == "O/U" or betType == "o/u"):

        # Get user's choice of over or under
        userInputOverOrUnder = input("\nOver or under?\n")
        listUserOverOrUnder = GetUserBetOnOverOrUnder(userInputOverOrUnder)

        # Get the chosen total
        betLine = GetUserTotalLine(betProvider, betting_api_instance, year, week, chosenTeam, conference)

        # Print chosen bet information
        print("\nThe chosen bet is {} {}".format(listUserOverOrUnder[1], betLine))

        # Get current score (home vs. vistor) and current total score
        homeVsVistorScore = GetHomeVsVisitorScore(betting_api_instance, year, week, chosenTeam, conference)
        totalScore = GetTotalScore(betting_api_instance, year, week, chosenTeam, conference)

        # Print score information
        PrintTotalBetCurrentScoreInfo(homeVsVistorScore,totalScore)

        # Calculate current cash
        userNewCash = CalculateCashFromTotalBet(userCurrentCash, userBetAmount, betLine, listUserOverOrUnder[0], totalScore)

    # Print final cash amount
    print("\n" + str(userFirstName) + " " + str(userLastName) + " currently has $" + str(userNewCash) + "\n")

    return()

# Run the main function
if __name__ == '__main__':
    main()