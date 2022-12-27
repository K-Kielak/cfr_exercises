import logging
import math

import click
import numpy as np

from cfre.blotto.blotto_bot import action_to_battlefields
from cfre.blotto.blotto_bot import BlottoBot, comb_with_repetition
from cfre.blotto.config import NUM_ROUNDS, NUM_SOLDIERS, NUM_BATTLEFIELDS
from cfre.blotto.config import PLOT_REFRESH_RATE
from cfre.utils.dynamic_plots import DynamicPlot, SubplotConfig

logger = logging.getLogger(__name__)


MAX_PLOTS_PER_COL = 5


@click.command(name='blotto')
def run_blotto_bot():
    logger.info(f'Running {NUM_ROUNDS} iterations of the Blotto game.')
    bot = BlottoBot(NUM_SOLDIERS, NUM_BATTLEFIELDS)
    plot = _create_dynamic_plot()
    for i in range(NUM_ROUNDS):
        action1 = bot.act()
        action2 = bot.act(perform_update=False)
        bot.update_regret(action2)

        if i % PLOT_REFRESH_RATE == 0:
            plot.update(np.full(bot.avg_strategy.shape, i), bot.avg_strategy)

    plot.save('blotto.png')

def _create_dynamic_plot() -> DynamicPlot:
    num_pure_strategies = comb_with_repetition(NUM_SOLDIERS, NUM_BATTLEFIELDS)
    configs = []
    for i in range(1, num_pure_strategies + 1):
        strategy = action_to_battlefields(i, NUM_SOLDIERS, NUM_BATTLEFIELDS)
        conf = SubplotConfig(f'Probability of {list(strategy)}', y_range=(0, 1))
        configs.append(conf)

    cols = int(math.ceil(num_pure_strategies / MAX_PLOTS_PER_COL))
    return DynamicPlot(configs, cols)
