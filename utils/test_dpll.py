
def test_dpll():
    """This is also tested in test_dimacs"""
    A, B, C = symbols('A,B,C')
    assert dpll([A | B], [A, B], {A: True, B: True}) == {A: True, B: True}

