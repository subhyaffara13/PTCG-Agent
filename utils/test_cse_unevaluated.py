
def test_cse_unevaluated():
    xp1 = UnevaluatedExpr(x + 1)
    # This used to cause RecursionError
    [(x0, ue)], [red] = cse([(-1 - xp1) / (1 - xp1)])
    if ue == xp1:
        assert red == (-1 - x0) / (1 - x0)
    elif ue == -xp1:
        assert red == (-1 + x0) / (1 + x0)
    else:
        msg = f'Expected common subexpression {xp1} or {-xp1}, instead got {ue}'
        assert False, msg

