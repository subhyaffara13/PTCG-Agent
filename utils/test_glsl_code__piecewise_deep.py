
def test_glsl_code_Piecewise_deep():
    p = glsl_code(2*Piecewise((x, x < 1), (x**2, True)))
    s = \
"""\
2*((x < 1) ? (
   x
)
: (
   pow(x, 2.0)
))\
"""
    assert p == s

