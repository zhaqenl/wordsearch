from nose.tools import *
import core
import input_data

def test_amount():
    assert_equal(core.wordsearch('xkxxxxxxx', input_data.xk_grid), 3325)

def test_list():
    assert_equal(core.find_matches('cat', input_data.special_grid), [[(0, 0), (0, 1), (0, 2)],
                                                                     [(0, 0), (1, 0), (2, 0)],
                                                                     [(0, 0), (1, 1), (2, 2)],
                                                                     [(2, 3), (1, 3), (0, 3)]])
