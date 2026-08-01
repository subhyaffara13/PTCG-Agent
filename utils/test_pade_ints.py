
def test_pade_ints():
    # Simple test sequences (one of ints, one of floats).
    an_int = [1, 2, 3, 4]
    an_flt = [1.0, 2.0, 3.0, 4.0]

    # Make sure integer arrays give the same result as float arrays with same values.
    for i in range(0, len(an_int)):
        for j in range(0, len(an_int) - i):

            # Create float and int pade approximation for given order.
            nump_int, denomp_int = pade(an_int, i, j)
            nump_flt, denomp_flt = pade(an_flt, i, j)

            # Check that they are the same.
            xp_assert_equal(nump_int.c, nump_flt.c)
            xp_assert_equal(denomp_int.c, denomp_flt.c)

