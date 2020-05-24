from typing import Dict

import logging

import click

from cfre.kuhn.information_set import InformationSet
from cfre.kuhn.kuhn_trainer import KuhnTrainer
from cfre.kuhn.config import LOGGING_FREQUENCY, NUM_ROUNDS

logger = logging.getLogger(__name__)


@click.command(name='kuhn')
def run_kuhn_trainer():
    logger.info(f'Running {NUM_ROUNDS} iterations of the CFR for Kuhn Poker.')
    trainer = KuhnTrainer()
    total_reward = 0
    for i in range(NUM_ROUNDS):
        total_reward += trainer.play_round()
        if i % LOGGING_FREQUENCY == 0:
            logger.info(f'Round {i}:')
            pretty_infosets = infosets_to_pretty_str(trainer.information_sets)
            logger.info(f'Information sets: {pretty_infosets}')
            logger.info(f'Average reward: {total_reward / (i + 1)}')
            logger.info('****************\n')


def infosets_to_pretty_str(infosets: Dict[str, InformationSet]):
    out = '{\n'
    for hist, iset in infosets.items():
        out += f'\t{hist}: {iset.avg_strategy}\n'

    return out + '}'
