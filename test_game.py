from Table import Table

# GAME SETTING
STARTING_CASH = 1000
MINIMUM_NUMBER_OF_PLAYERS = 2
MAXIMUM_NUMBER_OF_PLAYERS = 5
SMALL_BLIND_VALUE = 5
BIG_BLIND_VALUE = 10

# GAME CONFIGURATION


if __name__ == '__main__':
    players_names = ['Player1', 'Player2']
    table = Table(SMALL_BLIND_VALUE, BIG_BLIND_VALUE, STARTING_CASH)
    for name in players_names:
        table.register_player(name)


