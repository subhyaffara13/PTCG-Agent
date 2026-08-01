
def test_fuzzy_nand():
    for args in [(1, 0), (1, 1), (0, 0)]:
        assert fuzzy_nand(args) == fuzzy_not(fuzzy_and(args))

