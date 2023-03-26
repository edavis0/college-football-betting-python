from cfbd.rest import ApiException

# Returns the current game score as a string
def GetHomeVsVisitorScore(api_instance, year, week, team, conference):
    try:
        # Retrieve API response
        apiResponse = api_instance.get_lines(year = year, week = week, team = team, conference = conference)

        # Print game score information to the console
        homeVsVistorScore = "{} {} - {} {}".format(apiResponse[0].home_team,apiResponse[0].home_score,apiResponse[0].away_team,apiResponse[0].away_score)

    except ApiException as e:
        print("Exception when calling BettingApi->get_lines: %s\n" % e)
    return(homeVsVistorScore)