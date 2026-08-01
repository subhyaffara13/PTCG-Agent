
def test_eval_chebyt_gh20129():
    # https://github.com/scipy/scipy/issues/20129
    assert _ufuncs.eval_chebyt(7, 2 + 0j) == 5042.0

