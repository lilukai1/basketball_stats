from constants import PLAYERS
from constants import TEAMS
import copy

import pdb
import random

players = copy.deepcopy(PLAYERS)
teams= copy.deepcopy(TEAMS)

experienced_players = []
inexperienced_players = []
team_roster = {'Warriors':[], 'Bandits':[], 'Panthers':[]}
team_height = {'Warriors':int(), 'Bandits':int(), 'Panthers':int()}

def clean_data():
    for player in players:
        if player['experience'] == 'YES':
            player['experience'] = True
            experienced_players.append(player)
        else:
            player['experience'] = False
            inexperienced_players.append(player)

        player['height'] = player['height'].strip(" inches")
        player['height'] = int(player['height'])
        player['team'] = None
        player['guardians'] = player['guardians'].split(" and ")


## Made this a reusable function.  This way any criteria from any user defined list
## can be passed in and sorted.  Just make a list and send it to the function.  It
## will sort players in the list evenly among the specified teams.  This also randomly
## divides players so random matchups could be used for pickup games.

def balance_teams(player_list):
    team_choices = copy.deepcopy(teams)
    roster_player_count = dict.fromkeys(teams, 0)
    players_per_team = (len(player_list)/len(teams))
    
    for player in player_list:
        team_choice = random.choice(team_choices)
        player['team'] = team_choice
        roster_player_count[team_choice] += 1
        team_roster[team_choice].append(player)
        team_height[team_choice] += player['height']
        # print(f"{player} choose {team_choice}") ## for debugging or viewing player assignments live.
        if roster_player_count[team_choice] == players_per_team:
            team_choices.remove(team_choice)
            # print(f"removing {team_choice} with {roster_player_count[team_choice]} players") ## for debugging


def main_menu():
    basic_options = """
    1.  Show Stats 
    2.  Quit 
    """
    print(basic_options)
    ## https://medium.com/better-programming/how-to-indefinitely-request-user-input-until-valid-in-python-388a7c85aa6e
    ## this article from medium helped me understand how to make this work
    while True:
        try:
            option = int(input("Please choose your option, using the number >>>   "))
            if option in [1, 2]:
                break
        except:
            print("That's not a valid option!\n")

    if option == 2:
        print("Thank you, have a great day!")
        exit()
    else:
        team_menu()


def team_menu():
    team_options = list(enumerate(teams, start=1))
    print("\n")

    for num, team in team_options:
        print(f"{num}. {team}")
    
    print("\n")

    while True:
        try:
            team_option = int(input("Great, which team would you like to view? >>>   "))
            if team_option in range(len(team_options)+1):                           ############################
                break
            print("I'm sorry, thats not an available option.")
        except:
            print("I'm sorry, thats not an available option.")
    
    team_option = dict(team_options)[team_option]

    team_count = len(team_roster[team_option])
    exp_players = []
    inexp_players=[]
    for player in team_roster[team_option]:
        if player['experience']:
            exp_players.append(player)
        else:
            inexp_players.append(player)
    
    team_guards = ""
    team_players = ""
    for player in team_roster[team_option]:
        team_players += f"{player['name']}, "
        for guardian in  player['guardians']:
            team_guards += f"{guardian}, "
    team_players = team_players[:-2]
    team_guards = team_guards[:-2]

    player_print = f"""
{team_option}'s Stats
~~~~~~~~~~~~~~~~~~~~~
Experienced players: {len(exp_players)}
Inexperienced Players: {len(inexp_players)}
Average height of all players: {team_height[team_option]/team_count :.2f}

The {team_count} players for {team_option}:
{team_players}

Guardians:      
{team_guards}
"""
    print(player_print)

    continue_program = input("Press any key to continue....\n")
    main_menu()


if __name__ == "__main__":

    clean_data()
    balance_teams(experienced_players)
    balance_teams(inexperienced_players)

    welcome = """
Welcome to Basketball Stats
~~~~~~~~~~~~~~~~~~~~~~~~~~~\n
What would you like to do? """
    print(welcome)


    main_menu()