
def test_hyper_rewrite_sum():
    from sympy.concrete.summations import Sum
    from sympy.core.symbol import Dummy
    from sympy.functions.combinatorial.factorials import (RisingFactorial, factorial)
    _k = Dummy("k")
    assert replace_dummy(hyper((1, 2), (1, 3), x).rewrite(Sum), _k) == \
        Sum(x**_k / factorial(_k) * RisingFactorial(2, _k) /
            RisingFactorial(3, _k), (_k, 0, oo))

    assert hyper((1, 2, 3), (-1, 3), z).rewrite(Sum) == \
        hyper((1, 2, 3), (-1, 3), z)

