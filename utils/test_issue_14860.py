
def test_issue_14860():
    from sympy.physics.units import newton, kilo
    assert solve(8*kilo*newton + x + y, x) == [-8000*newton - y]

