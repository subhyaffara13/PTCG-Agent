
def test_all_or_nothing():
    x = symbols('x', extended_real=True)
    args = x >= -oo, x <= oo
    v = And(*args)
    if v.func is And:
        assert len(v.args) == len(args) - args.count(S.true)
    else:
        assert v == True
    v = Or(*args)
    if v.func is Or:
        assert len(v.args) == 2
    else:
        assert v == True

