
def test_pretty_ComplexRootOf():
    expr = rootof(x**5 + 11*x - 2, 0)
    ascii_str = \
"""\
       / 5              \\\n\
CRootOf\\x  + 11*x - 2, 0/\
"""
    ucode_str = \
"""\
       ⎛ 5              ⎞\n\
CRootOf⎝x  + 11⋅x - 2, 0⎠\
"""

    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

