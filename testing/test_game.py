from TableSys.Table import Table

from Enums import TestMode
from testing.scene_generator import SceneGenerator

# GAME SETTING
STARTING_CASH = 3000
MINIMUM_NUMBER_OF_PLAYERS = 2
MAXIMUM_NUMBER_OF_PLAYERS = 5
SMALL_BLIND_VALUE = 5
BIG_BLIND_VALUE = 10

# TEST CONFIGURATION
NUMBER_OF_REPEATS = 100
NUMBER_OF_SCENES = 1
TEST_MODE = TestMode.AUTOMATICALLY
if __name__ == '__main__':
    scene_generator = SceneGenerator()
    names = ['Omri', 'Bar', 'Ido']
    for repeat_index in range(0, NUMBER_OF_REPEATS):
        scene_generator.generate_scenes(NUMBER_OF_SCENES)
        for file_index in range(0, NUMBER_OF_SCENES):
            table = Table(SMALL_BLIND_VALUE, BIG_BLIND_VALUE, STARTING_CASH, TEST_MODE.value, file_index)
            for i in range(0, len(names)):
                table.register_player(names[i])
            table.init_table()
        print("#############FINISHED#####################")
        scene_generator.delete_scenes(NUMBER_OF_SCENES)
    #deck =Deck()
    #player_hand = deck.deal_cards()
    #  hand=[Card(14,0),Card(8,1),Card(5,2),Card(13,3),Card(12,0)]
    #  print(get_hand_combination_strength(hand))