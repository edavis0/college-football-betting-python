# crimsonboar


## Overview
This repository contains source code allowing the user to simulate betting on American college football games. It utilizes the [CFBD Python API][1]. For more information regarding the CFBD APIs and databases, please refer to this [link][2].

The following sections detail the process flow of the program and its relevant functions.

## Bet Types
Two bet types are used in this program: point spread bets and total point bets (also known as over/under bets). For more information regarding the mechanics of these bets, refer to this [link][3].

## Backlog of TODOs
* Refactor for code optimization
* Build a program flow diagram
* Add SQLite functionality to store user's bets
* Create a demonstration GIF
* Move this to a new public Github repository

## Program Diagram
TBD  

<br>

## _CatchAllFunctions.py
### **GetHomeVsVisitorScore(api_instance, year, week, team, conference)**

Returns the current game score as a string in the following form: 
`{home team name} {home team score} - {away team name} {away team score}`
Example: 

    Florida 29 - Alabama 31
<br>

## _PrintFunctions.py
### **PrintAllGamesBettingData(api_instance, year, week, conference)**

Prints betting information for every game in the user's chosen conference and week. This is printed to console in table form using the [Tabulate Python library][4].
Example: 

    +-----------+-----------+--------------+--------+------------+
    | Home Team | Away Team | Bet Provider | Spread | Over/Under |
    +-----------+-----------+--------------+--------+------------+
    +---------+---------+--------+---------------+------+
    | Florida | Alabama | Bovada | Alabama -14.5 | 60.5 |
    +---------+---------+--------+---------------+------+

### **PrintSingleGameBettingData(api_instance, year, week, team, conference)**

Prints betting information for a single game using the user's chosen year, week, team, and conference. This isn't used in the current iteration of `main.py`.  
Example: 

    Bet Provider	Spread		Over Under
    ------------------------------------------
    consensus:	Alabama -14	60
    numberfire:	Alabama -15.5	58.5
    teamrankings:	Alabama -14	59.5
    Bovada:	Alabama -14.5	60.5
    William Hill (New Jersey):	Alabama -14	60
<br>

## _SpreadFunctions.py
### **GetFavoredAndUnfavoredTeamList(betProvider, api_instance, year, week, team, conference)**

Returns a list of the favored and unfavored teams from the chosen bet. The list's format is as follows:  
`[favored team name string, unfavored team name string]`.  
Example:

    listFavoredAndUnfavoredTeams = [favoredTeam, unfavoredTeam]
    favoredTeam = 'Alabama'
    unfavoredTeam = 'Florida'

### **GetUserBetOnFavoredOrUnfavoredTeam(favoredTeam, team)**

Returns a boolean identifying if the user chose the favored team or not. If the user is betting on the favored team, the return boolean `betOnFavoredTeam` will be set to `True`. If the user is betting on the unfavored team, the return boolean `betOnFavoredTeam` will be set to `False`.

### **GetUserSpreadLine(betProvider, api_instance, year, week, team, conference, listFavoredAndUnfavoredTeams, betOnFavoredTeam)**

Returns the line of the chosen point spread as a floating point number.  
Example:

    chosenSpread = -14.5

### **PrintSpreadBettingInfo(betSpreadOrLine, listFavoredAndUnfavoredTeams, chosenTeam)**

Prints the user's chosen point spread betting information.  
Example:

    The chosen spread is -14.5
    The chosen team is Alabama
    Favored team: Alabama
    Unfavored team: Florida

### **GetScoreDifferentialList(api_instance, year, week, team, conference, favoredTeam)**

Returns a list of the the game score differential information. The list's format is as follows: 
`[score differential integer, formatted score differential string, favored team score integer, unfavored team score integer]`  
Example:

    listScoreInfo = [int(scoreDiff), formattedScoreDiff, int(favoredTeamScore), int(unfavoredTeamScore)]
    scoreDiff = -2
    formattedScoreDiff = 'Alabama is winning by 2 points'
    favoredTeamScore = 31
    unfavoredTeamScore = 29

### **PrintSpreadBetCurrentScoreInfo(homeVsVistorScore,listScoreDifferential)**
Prints the current score information.  
Example:

    Current Score: Florida 29 - Alabama 31
    Favored team score: 31
    Unfavored team score: 29
    Alabama is winning by 2 points

### **CalculateCashFromSpreadBet(currentCash, betAmount, betOnFavoredTeam, betSpread, scoreDiff)**
Returns an integer of the user's new cash amount after the game is complete.  
Example:

    newCash = 2750
<br>

## _TotalFunctions.py
### **GetUserBetOnOverOrUnder(userInputOverOrUnder)**  
Returns a list of the user's point total bet information. The list's format is as follows: `[user bet on over or under boolean, over or under string]`. If the user bets on the over, the `boolBetOnOver` will be set to `True`. If the user bets on the under, he `boolBetOnOver` will be set to `False`.
Example:

    listUserOverOrUnder = [boolBetOnOver, stringOverOrUnder]
    boolBetOnOver = True
    stringOverOrUnder = 'over'

### **GetUserTotalLine(betProvider, api_instance, year, week, team, conference)**
Returns the line of the user's point total bet as a floating point number.
Example:

    betLine = 60.5
<br>

### **GetTotalScore(api_instance, year, week, team, conference)**
Returns the total score score of the game as an integer. For example, if Florida scores 29 points and Alabama scores 31 points, the total score will be equal to 60 points.
Example:

    totalScore = 60
<br>

### **PrintTotalBetCurrentScoreInfo(homeVsVistorScore,totalScore)**
Prints the current or final score of the user's chosen total point bet. 
Example:

    Current Score: Florida 29 - Alabama 31
    Total Score: 60
<br>

### **CalculateCashFromTotalBet(currentCash, betAmount, betLine, betOnOver, actualTotalScore)**
Calculates the user's current cash based on the outcome of the point total bet.

## api_instance.get_lines Response Example
When the CFBD .get_lines method is executed, the following output is generated. The data type is a list.

    [{'away_conference': 'SEC',
    'away_score': 47,
    'away_team': 'Alabama',
    'home_conference': 'SEC',
    'home_score': 23,
    'home_team': 'South Carolina',
    'id': 401110794,
    'lines': [{'formattedSpread': 'Alabama -26.5',
                'overUnder': '59.5',
                'overUnderOpen': None,
                'provider': 'consensus',
                'spread': '26.5',
                'spreadOpen': None},
            {'formattedSpread': 'Alabama -26.5',
                'overUnder': '59',
                'overUnderOpen': None,
                'provider': 'Caesars',
                'spread': '26.5',
                'spreadOpen': None},
            {'formattedSpread': 'Alabama -26',
                'overUnder': '60',
                'overUnderOpen': None,
                'provider': 'numberfire',
                'spread': '26',
                'spreadOpen': None},
            {'formattedSpread': 'Alabama -25.5',
                'overUnder': '59.5',
                'overUnderOpen': None,
                'provider': 'teamrankings',
                'spread': '25.5',
                'spreadOpen': None}],
    'season': 2019,
    'season_type': 'regular',
    'week': 3}]


[1]: https://github.com/CFBD/cfbd-python "CFBD Python API"
[2]: https://collegefootballdata.com/ "CFBD Website"
[3]: https://betandbeat.com/betting/american-football/#:~:text=American%20Football%20Odds,-Odds%20refer%20to&text=There%20are%20three%20types%20of,thing%2C%20only%20in%20different%20formats. "Bet Types Explained"
[4]: https://pypi.org/project/tabulate/ "Tabulate Python Library"


