import pytest
import numpy as np
from hamcrest import assert_that, equal_to, calling, raises
from numpy import testing as npt

from cfre.blotto.blotto_bot import action_to_battlefields, comb_with_repetition

@pytest.mark.parametrize('action, soldiers, battlefields, expected_out', [
    (1, 10, 5, np.array([10, 0, 0, 0, 0])),
    (6, 3, 3, np.array([1, 0, 2])),
    (7, 3, 3, np.array([0, 3, 0])),
    (14, 3, 4, np.array([0, 1, 2, 0])),
    (17, 5, 3, np.array([0, 4, 1])),
    (15, 5, 4, np.array([2, 1, 1, 1]))
])
def test_actionToBattlefields_1f10n5(action, soldiers, battlefields, expected_out):
    npt.assert_array_equal(action_to_battlefields(action, soldiers, battlefields), expected_out)


def test_actionToBattlefields_actionTooBig():
    assert_that(calling(action_to_battlefields).with_args(22, 5, 3), raises(ValueError))


def test_actionToBattlefields_actionTooSmall():
    assert_that(calling(action_to_battlefields).with_args(0, 3, 3), raises(ValueError))


@pytest.mark.parametrize('elements, bins, expected_out', [
    (2, 2, 3),
    (2, 3, 6),
    (0, 5, 1),
    (11, 7, 12376)
])
def test_combWithRepetition(elements, bins, expected_out):
    assert_that(comb_with_repetition(elements, bins), equal_to(expected_out))