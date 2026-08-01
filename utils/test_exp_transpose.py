
def test_exp_transpose():
    assert transpose(exp(x)) == exp(transpose(x))

