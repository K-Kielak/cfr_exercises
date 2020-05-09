from random import random

import numpy as np


class BlottoBot:

    def __init__(self,
                 num_soldiers: int,
                 num_battlefields: int,
                 default_strategy: np.array = None):
        if num_soldiers < num_battlefields:
            raise ValueError(f'Number of soldiers {num_soldiers} '
                             f'has to be bigger than number of '
                             f'battlefields {num_battlefields}')

        self._num_soldiers = num_soldiers
        self._num_battlefields = num_battlefields
        self._num_pure_strategies = comb_with_repetition(num_soldiers,
                                                         num_battlefields)

        self._default_strategy = default_strategy
        if default_strategy is None:
            uniform_prob = 1 / self._num_pure_strategies
            self._default_strategy = np.full(self._num_pure_strategies, uniform_prob)

        if self._default_strategy.shape != (self._num_pure_strategies,):
            raise ValueError(f'Invalid shape of the initial strategy. Was'
                             f'{self._default_strategy.shape} but should be'
                             f'{(self._num_pure_strategies,)}')

        self._avg_strategy = np.zeros(self._num_pure_strategies)
        self._avg_reward = 0

        self._total_regret = np.zeros(self._num_pure_strategies)
        self._steps_num = 0
        self._prev_action = None

    def update_regret(self, opponent_action: int):
        reward = self._calculate_outcome(self._prev_action, opponent_action)
        self._avg_reward += (reward - self._avg_reward) / self._steps_num

        possible_actions = np.arange(1, self._num_pure_strategies+1)
        out_vec_func = np.vectorize(lambda s: self._calculate_outcome(s, opponent_action))
        regrets = out_vec_func(possible_actions) - reward
        self._total_regret += regrets

    def _calculate_outcome(self, act1: int, act2: int) -> int:
        battlefields1 = action_to_battlefields(act1,
                                               self._num_soldiers,
                                               self._num_battlefields)
        battlefields2 = action_to_battlefields(act2,
                                               self._num_soldiers,
                                               self._num_battlefields)
        player1_points = (battlefields1 > battlefields2).sum()
        player2_points = (battlefields2 > battlefields1).sum()
        return player1_points - player2_points

    def act(self, perform_update: bool = True) -> int:
        strategy = self._calculate_strategy()
        action = self._sample_action(strategy)

        if perform_update:
            self._steps_num += 1
            self._update_average_strategy(strategy)
            self._prev_action = action

        return action

    def _calculate_strategy(self) -> np.array:
        strategy = np.maximum(self._total_regret, 0)
        strategy_norm = np.sum(strategy)

        if strategy_norm > 0:
            return strategy / strategy_norm

        # If all regrets are non-positive, choose default strategy
        return self._default_strategy

    def _sample_action(self, strategy: np.array) -> int:
        threshold = random()
        return np.searchsorted(strategy.cumsum(), threshold)

    def _update_average_strategy(self, strategy: np.array):
        self._avg_strategy += (strategy - self._avg_strategy) / self._steps_num


def action_to_battlefields(action: int,
                           num_soldiers: int,
                           num_battlefields: int
                           ) -> np.array:
    if action < 1:
        raise ValueError(f'Action has to be at least 1 but was {action}')

    num_pure_strategies = comb_with_repetition(num_soldiers, num_battlefields)
    if action > num_pure_strategies:
        raise ValueError(f'Action index ({action}) out of bound '
                         f'(max {num_pure_strategies})')

    comb_id = action  # We want to find combination with ID `act`
    battlefields = np.zeros(num_battlefields)
    for field in range(1, num_battlefields+1):
        for s in range(num_soldiers, -1, -1):
            # Calculate how many remaining combinations there is
            # to choose from once we fix number of soldiers
            # on battlefield `field` to `s`
            remaining_combs = comb_with_repetition(num_soldiers - s,
                                                   num_battlefields - field)
            if comb_id <= remaining_combs:
                # Choose `s` soldiers for battlefield `field` if `comb_id`
                # is within remaining combinations after this decision
                battlefields[field - 1] = s  # field - 1 cause 0 indexing
                num_soldiers -= s
                # And move to the next battlefield
                break
            else:
                # Otherwise, skip all possible combinations if this decision
                # would have been made, and try next value for `s`
                comb_id -= remaining_combs
                assert s != 0, ('Bug: battlefield should ' 
                                'have been assigned already!')

    return battlefields


def comb_with_repetition(num_elements: int, num_bins: int) -> int:
    """
    Calculates (n+k-1)!/(n!*(k-1)!)
        where: n - num_elements, k - num_bins
    """
    total = 1
    # Calculate (n+k-1)! / n!
    for v in range(num_elements+1, num_elements+num_bins):
        total *= v

    # Calculate (k-1)!
    divisor = 1
    for v in range(2, num_bins):
        divisor *= v

    assert (total / divisor) % 1 == 0, ('Bug: result of combination with '
                                        'repetition should always be an integer!')

    return total // divisor