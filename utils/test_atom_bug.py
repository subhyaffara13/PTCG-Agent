
def test_atom_bug():
    from sympy.integrals.heurisch import heurisch
    assert heurisch(meijerg([], [], [1], [], x), x) is None

