from collections import defaultdict
from random import sample
from typing import Tuple, Dict

import numpy as np

from cfre.kuhn.information_set import InformationSet


### RULES OF THE GAME
# 1. Two players each bet 1 chip
# 2. There are three cards, each corresponding to one of the numbers: 1, 2, 3
# 3. One card is dealt to each of the players
# 4. Game starts with player one
# 5. Game alternates between player 1 and 2
# 6. Players can bet (1 chip only) or pass
# 7. If player passes after bet -> opponent takes all chips
# 8. After two consecutive passes or two consecutive bets player reveal their
#      cards and one with higher card takes all chips.


CARDS = [1, 2, 3]
NUM_ACTIONS = 2
VALUE_TO_ACTION = {0: 'p', 1: 'b'}


class KuhnTrainer:

    def __init__(self):
        self._cards = None
        self._info_sets = defaultdict(lambda: InformationSet(2))

    def play_round(self) -> float:
        self._cards = sample(CARDS, 2)
        return self._cfr('', (1, 1))

    def _cfr(self, history: str, player_probs: Tuple[float, float]):
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

        # Get (or create) information set for the player
        info_set_key = str(self._cards[player]) + history
        info_set = self._info_sets[info_set_key]

        # Recursively call CFR for each action
        weight = player_probs[player]
        strategy = info_set.get_strategy(weight)

        expected_action_rewards = np.zeros(NUM_ACTIONS)
        for a in range(NUM_ACTIONS):
            next_hist = history + VALUE_TO_ACTION[a]
            if player == 0:
                next_player_probs = (player_probs[0]*strategy[a], player_probs[1])
            else:
                next_player_probs = (player_probs[0], player_probs[1]*strategy[a])

            # negative CFR because recursive call calculates reward for an opponent
            expected_action_rewards[a] = -self._cfr(next_hist, next_player_probs)

        full_expected_reward = np.dot(strategy, expected_action_rewards)

        # Compute and accumulate regret for each action
        regret = expected_action_rewards - full_expected_reward
        weighted_regret = player_probs[opponent] * regret
        info_set.update_regret(weighted_regret)

        return full_expected_reward

    @property
    def information_sets(self) -> Dict[str, InformationSet]:
        return self._info_sets















