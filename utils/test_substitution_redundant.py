
def test_substitution_redundant():
    # the third and fourth solutions are redundant in the test below
    assert substitution([x**2 - y**2, z - 1], [x, z]) == \
           {(-y, 1), (y, 1), (-sqrt(y**2), 1), (sqrt(y**2), 1)}

    # the system below has three solutions. Two of the solutions
    # returned by substitution are redundant.
    res = substitution([x - y, y**3 - 3*y**2 + 1], [x, y])
    assert len(res) == 5

