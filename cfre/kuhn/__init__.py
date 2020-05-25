import logging

import click

from cfre.kuhn.information_set import InformationSet, infosets_to_pretty_str
from cfre.kuhn.information_set import load_infosets, save_infosets
from cfre.kuhn.kuhn_game import KuhnGame
from cfre.kuhn.kuhn_trainer import KuhnTrainer
from cfre.kuhn.config import LOGGING_FREQUENCY, NUM_ROUNDS

logger = logging.getLogger(__name__)


@click.command(name='train_kuhn')
@click.option('--savepath', '-s', type=click.Path(dir_okay=False, writable=True))
@click.option('--loadpath', '-l', type=click.Path(dir_okay=False, readable=True, exists=True))
def run_kuhn_trainer(savepath: str, loadpath: str):
    if loadpath is not None:
        logger.info(f'Creating trainer using preexisting infosets from {loadpath}.')
        infosets = load_infosets(loadpath)
        trainer = KuhnTrainer(infosets)
    else:
        logger.info(f'Creating trainer from scratch.')
        trainer = KuhnTrainer()

    logger.info(f'Running {NUM_ROUNDS} iterations of the CFR for Kuhn Poker.')

    total_reward = 0
    for i in range(NUM_ROUNDS):
        total_reward += trainer.play_round()
        if i % LOGGING_FREQUENCY == 0:
            infosets = trainer.information_sets

            logger.info(f'Round {i}:')
            logger.info(f'Information sets: {infosets_to_pretty_str(infosets)}')
            logger.info(f'Average reward: {total_reward / (i + 1)}')
            if savepath is not None:
                logger.info(f'Saving infosets to {savepath}.')
                save_infosets(infosets, savepath)
            logger.info('****************\n')


@click.command(name='play_kuhn')
@click.option('--loadpath', '-l', type=click.Path(dir_okay=False, readable=True, exists=True), required=True)
def run_kuhn_game(loadpath: str):
    print(f'Loading pre-existing strategies from: {loadpath}')
    infosets = load_infosets(loadpath)
    game = KuhnGame(infosets)

    cont = 'y'
    num_games = 0
    total_reward = 0
    while cont != 'n':
        print(f'\nStarting game {num_games+1}')
        reward = game.start_game(num_games % 2)
        total_reward += reward
        num_games += 1

        print(f'Reward from game {num_games}: {reward}')
        print(f'Total reward so far: {total_reward} '
              f'(average: {total_reward / num_games})')
        cont = input('Do you want to continue? (n for no) ')

    print('\nThanks for playing!')
