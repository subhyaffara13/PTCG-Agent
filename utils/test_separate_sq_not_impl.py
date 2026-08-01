
def test_separate_sq_not_impl():
    raises(NotImplementedError, lambda: _separate_sq(x**(S(1)/3) + x))

