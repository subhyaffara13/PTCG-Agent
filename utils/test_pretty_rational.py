
def test_pretty_rational():
    expr = y*x**-2
    ascii_str = \
"""\
y \n\
--\n\
 2\n\
x \
"""
    ucode_str = \
"""\
y \n\
──\n\
 2\n\
x \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = y**Rational(3, 2) * x**Rational(-5, 2)
    ascii_str = \
"""\
 3/2\n\
y   \n\
----\n\
 5/2\n\
x   \
"""
    ucode_str = \
"""\
 3/2\n\
y   \n\
────\n\
 5/2\n\
x   \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = sin(x)**3/tan(x)**2
    ascii_str = \
"""\
   3   \n\
sin (x)\n\
-------\n\
   2   \n\
tan (x)\
"""
    ucode_str = \
"""\
   3   \n\
sin (x)\n\
───────\n\
   2   \n\
tan (x)\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

