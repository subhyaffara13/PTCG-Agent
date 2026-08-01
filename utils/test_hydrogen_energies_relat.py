
def test_hydrogen_energies_relat():
    # First test exact formulas for small "c" so that we get nice expressions:
    assert E_nl_dirac(2, 0, Z=1, c=1) == 1/sqrt(2) - 1
    assert simplify(E_nl_dirac(2, 0, Z=1, c=2) - ( (8*sqrt(3) + 16)
                / sqrt(16*sqrt(3) + 32) - 4)) == 0
    assert simplify(E_nl_dirac(2, 0, Z=1, c=3) - ( (54*sqrt(2) + 81)
                / sqrt(108*sqrt(2) + 162) - 9)) == 0

    # Now test for almost the correct speed of light, without floating point
    # numbers:
    assert simplify(E_nl_dirac(2, 0, Z=1, c=137) - ( (352275361 + 10285412 *
        sqrt(1173)) / sqrt(704550722 + 20570824 * sqrt(1173)) - 18769)) == 0
    assert simplify(E_nl_dirac(2, 0, Z=82, c=137) - ( (352275361 + 2571353 *
        sqrt(12045)) / sqrt(704550722 + 5142706*sqrt(12045)) - 18769)) == 0

    # Test using exact speed of light, and compare against the nonrelativistic
    # energies:
    for n in range(1, 5):
        for l in range(n):
            assert feq(E_nl_dirac(n, l), E_nl(n), 1e-5, 1e-5)
            if l > 0:
                assert feq(E_nl_dirac(n, l, False), E_nl(n), 1e-5, 1e-5)

    Z = 2
    for n in range(1, 5):
        for l in range(n):
            assert feq(E_nl_dirac(n, l, Z=Z), E_nl(n, Z), 1e-4, 1e-4)
            if l > 0:
                assert feq(E_nl_dirac(n, l, False, Z), E_nl(n, Z), 1e-4, 1e-4)

    Z = 3
    for n in range(1, 5):
        for l in range(n):
            assert feq(E_nl_dirac(n, l, Z=Z), E_nl(n, Z), 1e-3, 1e-3)
            if l > 0:
                assert feq(E_nl_dirac(n, l, False, Z), E_nl(n, Z), 1e-3, 1e-3)

    # Test the exceptions:
    raises(ValueError, lambda: E_nl_dirac(0, 0))
    raises(ValueError, lambda: E_nl_dirac(1, -1))
    raises(ValueError, lambda: E_nl_dirac(1, 0, False))

