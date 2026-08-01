
def test_rewrite_MaxMin_as_Piecewise():
    from sympy.core.symbol import symbols
    from sympy.functions.elementary.piecewise import Piecewise
    x, y, z, a, b = symbols('x y z a b', real=True)
    vx, vy, va = symbols('vx vy va')
    assert Max(a, b).rewrite(Piecewise) == Piecewise((a, a >= b), (b, True))
    assert Max(x, y, z).rewrite(Piecewise) == Piecewise((x, (x >= y) & (x >= z)), (y, y >= z), (z, True))
    assert Max(x, y, a, b).rewrite(Piecewise) == Piecewise((a, (a >= b) & (a >= x) & (a >= y)),
        (b, (b >= x) & (b >= y)), (x, x >= y), (y, True))
    assert Min(a, b).rewrite(Piecewise) == Piecewise((a, a <= b), (b, True))
    assert Min(x, y, z).rewrite(Piecewise) == Piecewise((x, (x <= y) & (x <= z)), (y, y <= z), (z, True))
    assert Min(x,  y, a, b).rewrite(Piecewise) ==  Piecewise((a, (a <= b) & (a <= x) & (a <= y)),
        (b, (b <= x) & (b <= y)), (x, x <= y), (y, True))

    # Piecewise rewriting of Min/Max does also takes place for not explicitly real arguments
    assert Max(vx, vy).rewrite(Piecewise) == Piecewise((vx, vx >= vy), (vy, True))
    assert Min(va, vx, vy).rewrite(Piecewise) == Piecewise((va, (va <= vx) & (va <= vy)), (vx, vx <= vy), (vy, True))

