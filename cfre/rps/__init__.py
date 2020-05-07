import logging
from typing import Optional, List

import click

from cfre.utils.dynamic_plots import DynamicPlot, SubplotConfig
from cfre.rps.config import NUM_ROUNDS, PLOT_REFRESH_RATE, OPPONENT_STRATEGY
from cfre.rps.rps_bot import RPSBot, sample_action


logger = logging.getLogger(__name__)
ACTIONS_MAP = {0: 'R', 1: 'P', 2: 'S'}


@click.command(name='rps')
def run_rps_bot():
    logger.info(f'Running {NUM_ROUNDS} iterations of the Rock-Paper-Scissors.')
    # Start with chossing always rock as a initial strategy
    bot = RPSBot(initial_strategy=[1, 0, 0])
    plot = _create_dynamic_plot()
    for i in range(NUM_ROUNDS):
        action1 = bot.act()
        if OPPONENT_STRATEGY is None:
            action2 = bot.act(perform_update=False)
        else:
            action2 = sample_action(OPPONENT_STRATEGY)

        bot.update_regret(action2)
        if i % PLOT_REFRESH_RATE == 0:
            plot.update([i] * 3, bot.avg_strategy)

    logger.info(f'Final strategy: {bot.avg_strategy}')
    input('Enter anything to close.')


def _create_dynamic_plot():
    rock_config = SubplotConfig('Probability of choosing rock', y_range=(0, 1))
    paper_config = SubplotConfig('Probability of choosing paper', y_range=(0, 1))
    scissors_config = SubplotConfig('Probability of choosing scissors', y_range=(0, 1))
    return DynamicPlot([rock_config, paper_config, scissors_config])