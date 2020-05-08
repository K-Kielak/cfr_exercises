import numpy as np


def action_to_battlefields(action: int,
                           num_soldiers: int,
                           num_battlefields: int
                           ) -> np.array:
    if action < 1:
        raise ValueError(f'Action has to be at least 1 but was {action}')

    num_pure_strategies = comb_with_repetition(num_soldiers, num_battlefields)
    if action > num_pure_strategies:
        raise ValueError(f'Action index ({action}) out of bound '
                         f'(max {num_pure_strategies})')

    comb_id = action  # We want to find combination with ID `act`
    battlefields = np.zeros(num_battlefields)
    for field in range(1, num_battlefields+1):
        for s in range(num_soldiers, -1, -1):
            # Calculate how many remaining combinations there is
            # to choose from once we fix number of soldiers
            # on battlefield `field` to `s`
            remaining_combs = comb_with_repetition(num_soldiers - s,
                                                   num_battlefields - field)
            if comb_id <= remaining_combs:
                # Choose `s` soldiers for battlefield `field` if `comb_id`
                # is within remaining combinations after this decision
                battlefields[field - 1] = s  # field - 1 cause 0 indexing
                num_soldiers -= s
                # And move to the next battlefield
                break
            else:
                # Otherwise, skip all possible combinations if this decision
                # would have been made, and try next value for `s`
                comb_id -= remaining_combs
                assert s != 0, ('Bug: battlefield should ' 
                                'have been assigned already!')

    return battlefields


def comb_with_repetition(num_elements: int, num_bins: int) -> int:
    """
    Calculates (n+k-1)!/(n!*(k-1)!)
        where: n - num_elements, k - num_bins
    """
    total = 1
    # Calculate (n+k-1)! / n!
    for v in range(num_elements+1, num_elements+num_bins):
        total *= v

    # Calculate (k-1)!
    divisor = 1
    for v in range(2, num_bins):
        divisor *= v

    assert (total / divisor) % 1 == 0, ('Bug: result of combination with '
                                        'repetition should always be an integer!')

    return total // divisor