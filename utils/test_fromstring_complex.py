
def test_fromstring_complex():
    for ctype in ["complex", "cdouble"]:
        # Check spacing between separator
        assert_equal(np.fromstring("1, 2 ,  3  ,4", sep=",", dtype=ctype),
                     np.array([1., 2., 3., 4.]))
        # Real component not specified
        assert_equal(np.fromstring("1j, -2j,  3j, 4e1j", sep=",", dtype=ctype),
                     np.array([1.j, -2.j, 3.j, 40.j]))
        # Both components specified
        assert_equal(np.fromstring("1+1j,2-2j, -3+3j,  -4e1+4j", sep=",", dtype=ctype),
                     np.array([1. + 1.j, 2. - 2.j, - 3. + 3.j, - 40. + 4j]))
        # Spaces at wrong places
        with assert_raises(ValueError):
            np.fromstring("1+2 j,3", dtype=ctype, sep=",")
        with assert_raises(ValueError):
            np.fromstring("1+ 2j,3", dtype=ctype, sep=",")
        with assert_raises(ValueError):
            np.fromstring("1 +2j,3", dtype=ctype, sep=",")
        with assert_raises(ValueError):
            np.fromstring("1+j", dtype=ctype, sep=",")
        with assert_raises(ValueError):
            np.fromstring("1+", dtype=ctype, sep=",")
        with assert_raises(ValueError):
            np.fromstring("1j+1", dtype=ctype, sep=",")

