from random import random
from typing import List


class RPSBot:

    def __init__(self, initial_strategy: List[float] = None):
        self._initial_strategy = initial_strategy
        if initial_strategy is None:
            # Default to uniformly mixed strategy
            self._initial_strategy = [1/3, 1/3, 1/3]

        self._avg_strategy = [0, 0, 0]
        self._avg_reward = 0

        self._total_regret = [0, 0, 0]
        self._steps_num = 0
        self._prev_action = None

    def update_regret(self, opponent_action: int):
        reward = calculate_outcome(self._prev_action, opponent_action)
        self._avg_reward += (reward - self._avg_reward) / self._steps_num

        for i in range(len(self._total_regret)):
            regret = calculate_outcome(i, opponent_action) - reward
            self._total_regret[i] += regret

    def act(self, perform_update: bool = True) -> int:
        strategy = self._calculate_strategy()
        action = sample_action(strategy)

        if perform_update:
            self._steps_num += 1
            self._update_average_strategy(strategy)
            self._prev_action = action

        return action

    def _calculate_strategy(self) -> List[float]:
        strategy = [max(r, 0) for r in self._total_regret]
        strategy_norm = sum(strategy)
        if strategy_norm > 0:
            return [s / strategy_norm for s in strategy]

        # If all regrets are non-positive, choose rock
        strategy = [1, 0, 0]
        strategy_norm = sum(strategy)
        return [s / strategy_norm for s in strategy]

    def _update_average_strategy(self, strategy: List[float]):
        self._avg_strategy = [avg + (s - avg) / self._steps_num
                              for avg, s in zip(self._avg_strategy, strategy)]

    @property
    def avg_strategy(self) -> List[float]:
        return self._avg_strategy

    @property
    def avg_reward(self) -> float:
        return self._avg_reward


def sample_action(strategy: List[int]) -> int:
    rand = random()
    probs_sum = 0
    action = -1
    for prob in strategy:
        action += 1
        probs_sum += prob
        if rand < probs_sum:
            break

    return action


def calculate_outcome(act1: int, act2: int) -> int:
    if act1 == act2:
        return 0

    if (act1 + 1) % 3 == act2:
        return -1

    return 1
