
def test_pretty_KroneckerDelta():
    x, y = symbols("x, y")
    expr = KroneckerDelta(x, y)
    ascii_str = \
"""\
d   \n\
 x,y\
"""
    ucode_str = \
"""\
δ   \n\
 x,y\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

