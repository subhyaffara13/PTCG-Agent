
def test_jscode_Piecewise():
    expr = Piecewise((x, x < 1), (x**2, True))
    p = jscode(expr)
    s = \
"""\
((x < 1) ? (
   x
)
: (
   Math.pow(x, 2)
))\
"""
    assert p == s
    assert jscode(expr, assign_to="c") == (
    "if (x < 1) {\n"
    "   c = x;\n"
    "}\n"
    "else {\n"
    "   c = Math.pow(x, 2);\n"
    "}")
    # Check that Piecewise without a True (default) condition error
    expr = Piecewise((x, x < 1), (x**2, x > 1), (sin(x), x > 0))
    raises(ValueError, lambda: jscode(expr))

