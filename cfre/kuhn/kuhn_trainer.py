from collections import defaultdict
from random import sample
from typing import Tuple, Dict

import numpy as np

from cfre.kuhn.information_set import InformationSet
from cfre.kuhn.kuhn_game import CARDS, NUM_ACTIONS, VALUE_TO_ACTION


class KuhnTrainer:

    def __init__(self, infosets=None):
        self._cards = None
        self._infosets = infosets
        if self._infosets is None:
            self._infosets = defaultdict(_new_kuhn_info_set)

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
        info_set = self._infosets[info_set_key]

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

            # Negative CFR because recursive call calculates reward for an opponent
            expected_action_rewards[a] = -self._cfr(next_hist, next_player_probs)

        full_expected_reward = np.dot(strategy, expected_action_rewards)

        # Compute and accumulate regret for each action
        regret = expected_action_rewards - full_expected_reward
        weighted_regret = player_probs[opponent] * regret
        info_set.update_regret(weighted_regret)

        return full_expected_reward

    @property
    def information_sets(self) -> Dict[str, InformationSet]:
        return self._infosets


def _new_kuhn_info_set():  # Use instead of lambda so it's picklable
    return InformationSet(2)












