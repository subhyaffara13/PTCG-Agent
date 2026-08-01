
def test_novalue():
    import numpy as np
    for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
        assert_equal(repr(np._NoValue), '<no value>')
        assert_(pickle.loads(pickle.dumps(np._NoValue,
                                          protocol=proto)) is np._NoValue)

