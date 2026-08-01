
def test_pretty_Subs():
    f = Function('f')
    expr = Subs(f(x), x, ph**2)
    ascii_str = \
"""\
(f(x))|     2\n\
      |x=phi \
"""
    unicode_str = \
"""\
(f(x))│   2\n\
      │x=φ \
"""

    assert pretty(expr) == ascii_str
    assert upretty(expr) == unicode_str

    expr = Subs(f(x).diff(x), x, 0)
    ascii_str = \
"""\
/d       \\|   \n\
|--(f(x))||   \n\
\\dx      /|x=0\
"""
    unicode_str = \
"""\
⎛d       ⎞│   \n\
⎜──(f(x))⎟│   \n\
⎝dx      ⎠│x=0\
"""

    assert pretty(expr) == ascii_str
    assert upretty(expr) == unicode_str

    expr = Subs(f(x).diff(x)/y, (x, y), (0, Rational(1, 2)))
    ascii_str = \
"""\
/d       \\|          \n\
|--(f(x))||          \n\
|dx      ||          \n\
|--------||          \n\
\\   y    /|x=0, y=1/2\
"""
    unicode_str = \
"""\
⎛d       ⎞│          \n\
⎜──(f(x))⎟│          \n\
⎜dx      ⎟│          \n\
⎜────────⎟│          \n\
⎝   y    ⎠│x=0, y=1/2\
"""

    assert pretty(expr) == ascii_str
    assert upretty(expr) == unicode_str

