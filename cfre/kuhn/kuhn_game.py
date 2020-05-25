from random import sample
from typing import Dict

from cfre.kuhn import InformationSet


CARDS = [1, 2, 3]
NUM_ACTIONS = 2
VALUE_TO_ACTION = {0: 'p', 1: 'b'}


class KuhnGame:

    def __init__(self, infosets: Dict[str, InformationSet]):
        self._infosets = infosets
        self._user_player = None
        self._cards = None

    def start_game(self, user_player=0):
        if user_player > 1 or user_player < 0:
            raise ValueError(f'User player can be either '
                             f'0 or 1 but was: {user_player}')

        self._user_player = user_player
        self._cards = sample(CARDS, 2)
        reward_modifier = 1 if user_player == 0 else -1
        return reward_modifier * self._play_game('')

    def _play_game(self, history: str):
        plays_so_far = len(history)
        player = plays_so_far % NUM_ACTIONS
        opponent = 1 - player

        # Check for terminal states
        if plays_so_far >= 2:
            card_comparison_util = 1 if self._cards[player] > self._cards[opponent] else -1
            last_two_plays = history[-2:]
            if last_two_plays == 'pp':
                return card_comparison_util

            if last_two_plays == 'bb':
                return 2 * card_comparison_util

            if last_two_plays == 'bp':
                return 1

        # Get player action
        info_set_key = str(self._cards[player]) + history
        if player == self._user_player:
            action = input(f'Current state: {info_set_key}. '
                           f'Choose your next action (p - pass, b - bet). ')
            while action not in VALUE_TO_ACTION.values():
                action = input(f'Invalid action. Was "{action}" but only one of '
                               f'{list(VALUE_TO_ACTION.values())} is possible.'
                               f'Choose again. ')
        else:
            action_key = self._infosets[info_set_key].sample_from_average_strategy()
            action = VALUE_TO_ACTION[action_key]

        # Negative because recursive call calculates reward for an opponent
        return -self._play_game(history + action)
