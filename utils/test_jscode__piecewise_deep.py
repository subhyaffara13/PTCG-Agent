
def test_jscode_Piecewise_deep():
    p = jscode(2*Piecewise((x, x < 1), (x**2, True)))
    s = \
"""\
2*((x < 1) ? (
   x
)
: (
   Math.pow(x, 2)
))\
"""
    assert p == s

