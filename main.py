import logging

import click

from cfre.blotto import run_blotto_bot
from cfre.kuhn import run_kuhn_trainer
from cfre.rps import run_rps_bot


@click.group()
@click.option('--debug', is_flag=True)
def cli(debug: bool):
    _setup_logging(debug)


def _setup_logging(debug: bool):
    level = logging.DEBUG if debug else logging.INFO
    message_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_formatter = logging.Formatter(fmt=message_format)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(level)
    logger = logging.getLogger('cfre')
    logger.setLevel(level)
    logger.addHandler(console_handler)
    logger.info(f'Debug mode is {"on" if debug else "off"}')


cli.add_command(run_rps_bot)
cli.add_command(run_blotto_bot)
cli.add_command(run_kuhn_trainer)


if __name__ == '__main__':
    cli()





