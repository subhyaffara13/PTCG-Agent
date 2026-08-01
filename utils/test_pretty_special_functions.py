
def test_pretty_special_functions():
    x, y = symbols("x y")

    # atan2
    expr = atan2(y/sqrt(200), sqrt(x))
    ascii_str = \
"""\
     /  ___         \\\n\
     |\\/ 2 *y    ___|\n\
atan2|-------, \\/ x |\n\
     \\  20          /\
"""
    ucode_str = \
"""\
     ⎛√2⋅y    ⎞\n\
atan2⎜────, √x⎟\n\
     ⎝ 20     ⎠\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

