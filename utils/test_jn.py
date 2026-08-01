
def test_jn():
    z = symbols("z")
    assert jn(0, 0) == 1
    assert jn(1, 0) == 0
    assert jn(-1, 0) == S.ComplexInfinity
    assert jn(z, 0) == jn(z, 0, evaluate=False)
    assert jn(0, oo) == 0
    assert jn(0, -oo) == 0

    assert mjn(0, z) == sin(z)/z
    assert mjn(1, z) == sin(z)/z**2 - cos(z)/z
    assert mjn(2, z) == (3/z**3 - 1/z)*sin(z) - (3/z**2) * cos(z)
    assert mjn(3, z) == (15/z**4 - 6/z**2)*sin(z) + (1/z - 15/z**3)*cos(z)
    assert mjn(4, z) == (1/z + 105/z**5 - 45/z**3)*sin(z) + \
        (-105/z**4 + 10/z**2)*cos(z)
    assert mjn(5, z) == (945/z**6 - 420/z**4 + 15/z**2)*sin(z) + \
        (-1/z - 945/z**5 + 105/z**3)*cos(z)
    assert mjn(6, z) == (-1/z + 10395/z**7 - 4725/z**5 + 210/z**3)*sin(z) + \
        (-10395/z**6 + 1260/z**4 - 21/z**2)*cos(z)

    assert expand_func(jn(n, z)) == jn(n, z)

    # SBFs not defined for complex-valued orders
    assert jn(2+3j, 5.2+0.3j).evalf() == jn(2+3j, 5.2+0.3j)

    assert eq([jn(2, 5.2+0.3j).evalf(10)],
              [0.09941975672 - 0.05452508024*I])

