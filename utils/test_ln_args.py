
def test_ln_args():
    assert O(log(x)) + O(log(2*x)) == O(log(x))
    assert O(log(x)) + O(log(x**3)) == O(log(x))
    assert O(log(x*y)) + O(log(x) + log(y)) == O(log(x) + log(y), x, y)

