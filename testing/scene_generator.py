from random import randrange
import os


class SceneGenerator:
    def generate_scenes(self, number_of_scenes):
        for i in range(0, number_of_scenes):
            f = open(f'scenes/simulation{i}.txt', "w+")
            print(f'creating file:simulation{i}.txt...')
            for row in range(0, 10000):
                if row < 9999:
                    random_choice = randrange(7)
                    if random_choice == 0 or random_choice == 1:
                        f.write("check\n")
                    elif random_choice == 2 or random_choice == 3:
                        f.write("call\n")
                    elif random_choice == 4 or random_choice == 5:
                        f.write("fold\n")
                    elif random_choice == 6:
                        random_raise = randrange(500)
                        f.write(f'raise {random_raise}\n')
                else:
                    random_choice = randrange(7)
                    if random_choice == 0 or random_choice == 1:
                        f.write("checkk\n")
                    elif random_choice == 2 or random_choice == 3:
                        f.write("calll\n")
                    elif random_choice == 4 or random_choice == 5:
                        f.write("foldd\n")
                    elif random_choice == 6:
                        random_raise = randrange(500)
                        f.write(f'raise {random_raise}n\n')
            f.close()

    def delete_scenes(self, number_of_scenes):
        for i in range(0, number_of_scenes):
            os.remove(f'scenes/simulation{i}.txt')
