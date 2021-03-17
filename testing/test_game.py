from Table import Table

from Enums import TestMode
from testing.scene_generator import SceneGenerator

# GAME SETTING
STARTING_CASH = 3000
MINIMUM_NUMBER_OF_PLAYERS = 2
MAXIMUM_NUMBER_OF_PLAYERS = 5
SMALL_BLIND_VALUE = 5
BIG_BLIND_VALUE = 10

# TEST CONFIGURATION
NUMBER_OF_SCENES = 10
TEST_MODE = TestMode.AUTOMATICALLY
if __name__ == '__main__':
    scene_generator = SceneGenerator()
    scene_generator.generate_scenes(NUMBER_OF_SCENES)
    names = ['Omri', 'Bar', 'Ido']
    for file_index in range(1, NUMBER_OF_SCENES+1):
        table = Table(SMALL_BLIND_VALUE, BIG_BLIND_VALUE, STARTING_CASH, TEST_MODE.value, file_index)
        for i in range(0, len(names)):
            table.register_player(names[i])
        table.init_table()
    print("#############FINISHED#####################")
    scene_generator.delete_scenes(NUMBER_OF_SCENES)
