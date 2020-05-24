from random import random

import numpy as np


class InformationSet:

    def __init__(self, num_actions):
        self._num_actions = num_actions

        self._total_weight = 0
        self._total_regret = np.zeros(self._num_actions)
        self._avg_strategy = np.zeros(self._num_actions)

    def update_regret(self, regret: np.array):
        self._total_regret += regret

    def sample_from_average_strategy(self) -> int:
        threshold = random()
        return np.searchsorted(self.avg_strategy.cumsum(), threshold)

    def get_strategy(self, realization_weight: float) -> np.array:
        strategy = np.maximum(self._total_regret, 0)
        strategy_norm = np.sum(strategy)
        if strategy_norm > 0:
            strategy = strategy / strategy_norm
        else:
            # If all regrets are non-positive, choose uniform random strategy
            strategy = np.full(self._num_actions, 1 / self._num_actions)

        self._update_average_strategy(strategy, realization_weight)
        return strategy

    def _update_average_strategy(self, strategy: np.array, realization_weight: float):
        self._total_weight += realization_weight
        strategy_diff = strategy - self._avg_strategy
        self._avg_strategy += realization_weight * strategy_diff / self._total_weight

    @property
    def avg_strategy(self) -> np.array:
        return self._avg_strategy
