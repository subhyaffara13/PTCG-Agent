
def test_issue_6359():
    assert pretty(Integral(x**2, x)**2) == \
"""\
          2
/  /     \\ \n\
| |      | \n\
| |  2   | \n\
| | x  dx| \n\
| |      | \n\
\\/       / \
"""
    assert upretty(Integral(x**2, x)**2) == \
"""\
         2
⎛⌠      ⎞ \n\
⎜⎮  2   ⎟ \n\
⎜⎮ x  dx⎟ \n\
⎝⌡      ⎠ \
"""

    assert pretty(Sum(x**2, (x, 0, 1))**2) == \
"""\
          2\n\
/ 1      \\ \n\
|___     | \n\
|\\  `    | \n\
| \\     2| \n\
| /    x | \n\
|/__,    | \n\
\\x = 0   / \
"""
    assert upretty(Sum(x**2, (x, 0, 1))**2) == \
"""\
          2
⎛  1     ⎞ \n\
⎜ ___    ⎟ \n\
⎜ ╲      ⎟ \n\
⎜  ╲    2⎟ \n\
⎜  ╱   x ⎟ \n\
⎜ ╱      ⎟ \n\
⎜ ‾‾‾    ⎟ \n\
⎝x = 0   ⎠ \
"""

    assert pretty(Product(x**2, (x, 1, 2))**2) == \
"""\
           2
/  2      \\ \n\
|______   | \n\
| |  |   2| \n\
| |  |  x | \n\
| |  |    | \n\
\\x = 1    / \
"""
    assert upretty(Product(x**2, (x, 1, 2))**2) == \
"""\
           2
⎛  2      ⎞ \n\
⎜─┬──┬─   ⎟ \n\
⎜ │  │   2⎟ \n\
⎜ │  │  x ⎟ \n\
⎜ │  │    ⎟ \n\
⎝x = 1    ⎠ \
"""

    f = Function('f')
    assert pretty(Derivative(f(x), x)**2) == \
"""\
          2
/d       \\ \n\
|--(f(x))| \n\
\\dx      / \
"""
    assert upretty(Derivative(f(x), x)**2) == \
"""\
          2
⎛d       ⎞ \n\
⎜──(f(x))⎟ \n\
⎝dx      ⎠ \
"""

