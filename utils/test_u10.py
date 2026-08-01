
def test_U10():
    # see issue 2519:
    assert residue((z**3 + 5)/((z**4 - 1)*(z + 1)), z, -1) == R(-9, 4)

