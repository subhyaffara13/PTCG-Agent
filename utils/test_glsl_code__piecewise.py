
def test_glsl_code_Piecewise():
    expr = Piecewise((x, x < 1), (x**2, True))
    p = glsl_code(expr)
    s = \
"""\
((x < 1) ? (
   x
)
: (
   pow(x, 2.0)
))\
"""
    assert p == s
    assert glsl_code(expr, assign_to="c") == (
    "if (x < 1) {\n"
    "   c = x;\n"
    "}\n"
    "else {\n"
    "   c = pow(x, 2.0);\n"
    "}")
    # Check that Piecewise without a True (default) condition error
    expr = Piecewise((x, x < 1), (x**2, x > 1), (sin(x), x > 0))
    raises(ValueError, lambda: glsl_code(expr))

