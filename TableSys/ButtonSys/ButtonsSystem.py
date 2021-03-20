from random import randrange

from TableSys.ButtonSys.Button import Button


class ButtonSystem:
    def __init__(self, small_blind_value, big_blind_value):
        self.dealer_button = Button(0)
        self.small_button = Button(small_blind_value)
        self.big_button = Button(big_blind_value)

    def init_buttons(self, names_of_players_remaining):
        random_play_index = randrange(len(names_of_players_remaining))
        if len(names_of_players_remaining) == 2:
            self.small_button.name = names_of_players_remaining[
                random_play_index % len(names_of_players_remaining)]
            self.big_button.name = names_of_players_remaining[
                (random_play_index + 1) % len(names_of_players_remaining)]
            self.dealer_button.name = "NO NEED"
            return self.small_button.name
        else:
            self.dealer_button.name = names_of_players_remaining[
                random_play_index % len(names_of_players_remaining)]
            self.small_button.name = names_of_players_remaining[
                (random_play_index + 1) % len(names_of_players_remaining)]
            self.big_button.name = names_of_players_remaining[
                (random_play_index + 2) % len(names_of_players_remaining)]
            return self.dealer_button.name

    def update_buttons(self, names_of_players_remaining, len_players):
        if len(names_of_players_remaining) == 2:
            if self.small_button.name != names_of_players_remaining[0]:
                self.small_button.name = names_of_players_remaining[0]
                self.big_button.name = names_of_players_remaining[1]
                self.dealer_button.name = "NO NEED"
                return  names_of_players_remaining[0]

            else:
                self.small_button.name = names_of_players_remaining[1]
                self.big_button.name = names_of_players_remaining[0]
                self.dealer_button.name = "NO NEED"
                return  names_of_players_remaining[1]

        elif len(names_of_players_remaining) > 2:
            self.dealer_button.name = names_of_players_remaining[
                (names_of_players_remaining.index(self.dealer_button.name) + 1) % len(
                    names_of_players_remaining)]
            self.small_button.name = names_of_players_remaining[
                (names_of_players_remaining.index(self.small_button.name) + 1) % len(
                    names_of_players_remaining)]
            self.big_button.name = names_of_players_remaining[
                (names_of_players_remaining.index(self.big_button.name) + 1) % len(
                    names_of_players_remaining)]
            return names_of_players_remaining[
                (names_of_players_remaining.index(self.dealer_button.name)) % len_players]
