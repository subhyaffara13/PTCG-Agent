
def test_issue_19427():
    # <https://github.com/sympy/sympy/issues/19427>
    x = Symbol("x")

    # Have always been okay:
    assert integrate((x ** 4) * sqrt(1 - x ** 2), (x, -1, 1)) == pi / 16
    assert integrate((-2 * x ** 2) * sqrt(1 - x ** 2), (x, -1, 1)) == -pi / 4
    assert integrate((1) * sqrt(1 - x ** 2), (x, -1, 1)) == pi / 2

    # Sum of the above, used to incorrectly return 0 for a while:
    assert integrate((x ** 4 - 2 * x ** 2 + 1) * sqrt(1 - x ** 2), (x, -1, 1)) == 5 * pi / 16

