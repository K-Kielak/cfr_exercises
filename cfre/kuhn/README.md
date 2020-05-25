# Counterfactual Regret Minimization (CFR) for Kuhn Poker

### Rules of the game
1. Two players each bet 1 chip
2. There are three cards, each corresponding to one of the numbers: 1, 2, 3
3. One card is dealt to each of the players
4. Game starts with player one
5. Game alternates between player 1 and 2
6. Players can bet (1 chip only) or pass
7. If player passes after bet -> opponent takes all chips
8. After two consecutive passes or two consecutive bets player reveal their
    cards and one with higher card takes all chips.
    
### Code
Code for the CFR for Kuhn Poker has two entry points:
1. `train_kuhn` - allows for running Monte Carlo CFR for Kuhn Poker to arrive
    at the most optimal strategies for each information set in the game.
2. `play_kuhn` - allows user to play the game against pre-trained strategies.

`cfre/kuhn/config.py` file allows user to specify number of training iterations 
and logging frequency for the training part of the code.