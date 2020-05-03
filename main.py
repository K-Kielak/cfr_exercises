from rps_bot import RPSBot


NUM_ROUNDS = 10000
ACTIONS_MAP = {0: 'R', 1: 'P', 2: 'S'}


def main():
    print(f'Running {NUM_ROUNDS} iterations of the game.')
    # Start with chossing always rock as a initial strategy
    bot = RPSBot(initial_strategy=[1, 0, 0])
    for i in range(NUM_ROUNDS):
        action1 = bot.act()
        action2 = bot.act(perform_update=False)
        bot.update_regret(action2)
        print(f'Strategy after round {i}: {bot.avg_strategy}')


if __name__ == '__main__':
    main()







