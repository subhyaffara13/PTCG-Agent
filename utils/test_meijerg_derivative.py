
def test_meijerg_derivative():
    assert meijerg([], [1, 1], [0, 0, x], [], z).diff(x) == \
        log(z)*meijerg([], [1, 1], [0, 0, x], [], z) \
        + 2*meijerg([], [1, 1, 1], [0, 0, x, 0], [], z)

    y = randcplx()
    a = 5  # mpmath chokes with non-real numbers, and Mod1 with floats
    assert td(meijerg([x], [], [], [], y), x)
    assert td(meijerg([x**2], [], [], [], y), x)
    assert td(meijerg([], [x], [], [], y), x)
    assert td(meijerg([], [], [x], [], y), x)
    assert td(meijerg([], [], [], [x], y), x)
    assert td(meijerg([x], [a], [a + 1], [], y), x)
    assert td(meijerg([x], [a + 1], [a], [], y), x)
    assert td(meijerg([x, a], [], [], [a + 1], y), x)
    assert td(meijerg([x, a + 1], [], [], [a], y), x)
    b = Rational(3, 2)
    assert td(meijerg([a + 2], [b], [b - 3, x], [a], y), x)

