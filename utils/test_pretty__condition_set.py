
def test_pretty_ConditionSet():
    ascii_str = '{x | x in (-oo, oo) and sin(x) = 0}'
    ucode_str = '{x │ x ∊ ℝ ∧ (sin(x) = 0)}'
    assert pretty(ConditionSet(x, Eq(sin(x), 0), S.Reals)) == ascii_str
    assert upretty(ConditionSet(x, Eq(sin(x), 0), S.Reals)) == ucode_str

    assert pretty(ConditionSet(x, Contains(x, S.Reals, evaluate=False), FiniteSet(1))) == '{1}'
    assert upretty(ConditionSet(x, Contains(x, S.Reals, evaluate=False), FiniteSet(1))) == '{1}'

    assert pretty(ConditionSet(x, And(x > 1, x < -1), FiniteSet(1, 2, 3))) == "EmptySet"
    assert upretty(ConditionSet(x, And(x > 1, x < -1), FiniteSet(1, 2, 3))) == "∅"

    assert pretty(ConditionSet(x, Or(x > 1, x < -1), FiniteSet(1, 2))) == '{2}'
    assert upretty(ConditionSet(x, Or(x > 1, x < -1), FiniteSet(1, 2))) == '{2}'

    condset = ConditionSet(x, 1/x**2 > 0)
    ascii_str = '''\
     1      \n\
{x | -- > 0}
      2     \n\
     x      '''
    ucode_str = '''\
⎧  │ ⎛1     ⎞⎫
⎪x │ ⎜── > 0⎟⎪
⎨  │ ⎜ 2    ⎟⎬
⎪  │ ⎝x     ⎠⎪
⎩  │         ⎭'''
    assert pretty(condset) == ascii_str
    assert upretty(condset) == ucode_str

    condset = ConditionSet(x, 1/x**2 > 0, S.Reals)
    ascii_str = '''\
                        1      \n\
{x | x in (-oo, oo) and -- > 0}
                         2     \n\
                        x      '''
    ucode_str = '''\
⎧  │         ⎛1     ⎞⎫
⎪x │ x ∊ ℝ ∧ ⎜── > 0⎟⎪
⎨  │         ⎜ 2    ⎟⎬
⎪  │         ⎝x     ⎠⎪
⎩  │                 ⎭'''
    assert pretty(condset) == ascii_str
    assert upretty(condset) == ucode_str

