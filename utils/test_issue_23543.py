
def test_issue_23543():
    # Used to give an error
    x, y, z = symbols("x y z", commutative=False)
    assert (x*(y + z/2)).simplify() == x*(2*y + z)/2

