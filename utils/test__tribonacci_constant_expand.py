
def test_TribonacciConstant_expand():
        assert TribonacciConstant.expand(func=True) == \
          (1 + cbrt(19 - 3*sqrt(33)) + cbrt(19 + 3*sqrt(33))) / 3

