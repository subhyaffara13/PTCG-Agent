
def test_pretty_RootSum():
    expr = RootSum(x**5 + 11*x - 2, auto=False)
    ascii_str = \
"""\
       / 5           \\\n\
RootSum\\x  + 11*x - 2/\
"""
    ucode_str = \
"""\
       ⎛ 5           ⎞\n\
RootSum⎝x  + 11⋅x - 2⎠\
"""

    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = RootSum(x**5 + 11*x - 2, Lambda(z, exp(z)))
    ascii_str = \
"""\
       / 5                   z\\\n\
RootSum\\x  + 11*x - 2, z -> e /\
"""
    ucode_str = \
"""\
       ⎛ 5                  z⎞\n\
RootSum⎝x  + 11⋅x - 2, z ↦ ℯ ⎠\
"""

    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

