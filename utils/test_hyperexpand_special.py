
def test_hyperexpand_special():
    assert hyperexpand(hyper([a, b], [c], 1)) == \
        gamma(c)*gamma(c - a - b)/gamma(c - a)/gamma(c - b)
    assert hyperexpand(hyper([a, b], [1 + a - b], -1)) == \
        gamma(1 + a/2)*gamma(1 + a - b)/gamma(1 + a)/gamma(1 + a/2 - b)
    assert hyperexpand(hyper([a, b], [1 + b - a], -1)) == \
        gamma(1 + b/2)*gamma(1 + b - a)/gamma(1 + b)/gamma(1 + b/2 - a)
    assert hyperexpand(meijerg([1 - z - a/2], [1 - z + a/2], [b/2], [-b/2], 1)) == \
        gamma(1 - 2*z)*gamma(z + a/2 + b/2)/gamma(1 - z + a/2 - b/2) \
        /gamma(1 - z - a/2 + b/2)/gamma(1 - z + a/2 + b/2)
    assert hyperexpand(hyper([a], [b], 0)) == 1
    assert hyper([a], [b], 0) != 0

