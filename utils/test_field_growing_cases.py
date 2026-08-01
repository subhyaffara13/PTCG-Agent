
def test_field_growing_cases():
    # Test empty field appending/growing (each field still takes 1 character)
    # to see if the final field appending does not create issues.
    res = np.loadtxt([""], delimiter=",", dtype=bytes)
    assert len(res) == 0

    for i in range(1, 1024):
        res = np.loadtxt(["," * i], delimiter=",", dtype=bytes, max_rows=10)
        assert len(res) == i + 1

