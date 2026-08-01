
def test_yn():
    z = symbols("z")
    assert myn(0, z) == -cos(z)/z
    assert myn(1, z) == -cos(z)/z**2 - sin(z)/z
    assert myn(2, z) == -((3/z**3 - 1/z)*cos(z) + (3/z**2)*sin(z))
    assert expand_func(yn(n, z)) == yn(n, z)

    # SBFs not defined for complex-valued orders
    assert yn(2+3j, 5.2+0.3j).evalf() == yn(2+3j, 5.2+0.3j)

    assert eq([yn(2, 5.2+0.3j).evalf(10)],
              [0.185250342 + 0.01489557397*I])

