
def test_sorted_args():
    x = symbols('x')
    assert b21._sorted_args == b21.args
    raises(AttributeError, lambda: x._sorted_args)

