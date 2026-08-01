
def test_tribonacci_constant_rewrite_as_sqrt():
    assert TribonacciConstant.rewrite(sqrt) == \
      (1 + cbrt(19 - 3*sqrt(33)) + cbrt(19 + 3*sqrt(33))) / 3

