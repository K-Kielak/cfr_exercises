import logging

import click

from cfre.blotto.blotto_bot import BlottoBot
from cfre.blotto.config import NUM_ROUNDS, NUM_SOLDIERS, NUM_BATTLEFIELDS


logger = logging.getLogger(__name__)


@click.command(name='blotto')
def run_blotto_bot():
    logger.info(f'Running {NUM_ROUNDS} iterations of the Blotto game.')
    bot = BlottoBot(NUM_SOLDIERS, NUM_BATTLEFIELDS)
    for i in range(NUM_ROUNDS):
        action1 = bot.act()
        action2 = bot.act(perform_update=False)
        bot.update_regret(action2)
        logger.info(f'Round {i}')
        logger.info(f'Average strategy: \n{bot.avg_strategy}')
        logger.info(f'Average reward: {bot.avg_reward}\n')
