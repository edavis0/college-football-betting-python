from cfbd.rest import ApiException
from tabulate import tabulate

# Print all game information based on conference and week
def PrintAllGamesBettingData(api_instance, year, week, conference):
    try:
        # Retrieve API response
        apiResponse = api_instance.get_lines(year = year, week = week, conference = conference)

        # Calculate length of the list containing betting data (Note: each element in apiResponse contains a list of betting data for each game)
        apiResponseLength = len(apiResponse)

        # Print search criteria and table headers
        print("\nYear: {}\tWeek: {}\t\tConference: {}\n".format(year, week, conference))
        print(tabulate([['Home Team', 'Away Team', 'Bet Provider', 'Spread', 'Over/Under']], tablefmt='pretty'))

        # Print betting information
        for i in range(apiResponseLength):
            listLines = apiResponse[i].lines
            homeTeam = apiResponse[i].home_team
            awayTeam = apiResponse[i].away_team

            for j in range(len(listLines)):
                
                # Pull out specific bet provider details and build a list to be printed
                betProvider = listLines[j]['provider']
                formattedSpread = listLines[j]['formattedSpread']
                overUnder = listLines[j]['overUnder']
                gameInfoList = [[homeTeam, awayTeam, betProvider, formattedSpread, overUnder]]

                print(tabulate(gameInfoList, tablefmt='pretty'))

    except ApiException as e:
        print("Exception when calling BettingApi->get_lines: %s\n" % e)
    return()

# Print point spread and over under data
def PrintSingleGameBettingData(api_instance, year, week, team, conference):
    try:
        # Retrieve API response
        apiResponse = api_instance.get_lines(year = year, week = week, team = team, conference = conference)

        # Assign game line information to a variable
        listOfLines = apiResponse[0].lines
        listLength = len(listOfLines)

        # Print betting information
        print("Bet Provider\tSpread\t\tOver Under")
        print('------------------------------------------')
        for i in range(listLength):
            print("{}:\t{}\t{}".format(listOfLines[i]['provider'], listOfLines[i]['formattedSpread'],listOfLines[i]['overUnder']))

    except ApiException as e:
        print("Exception when calling BettingApi->get_lines: %s\n" % e)
    return()