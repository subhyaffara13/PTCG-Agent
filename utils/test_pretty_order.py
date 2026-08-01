
def test_pretty_order():
    expr = O(1)
    ascii_str = \
"""\
O(1)\
"""
    ucode_str = \
"""\
O(1)\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = O(1/x)
    ascii_str = \
"""\
 /1\\\n\
O|-|\n\
 \\x/\
"""
    ucode_str = \
"""\
 ⎛1⎞\n\
O⎜─⎟\n\
 ⎝x⎠\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = O(x**2 + y**2)
    ascii_str = \
"""\
 / 2    2                  \\\n\
O\\x  + y ; (x, y) -> (0, 0)/\
"""
    ucode_str = \
"""\
 ⎛ 2    2                 ⎞\n\
O⎝x  + y ; (x, y) → (0, 0)⎠\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = O(1, (x, oo))
    ascii_str = \
"""\
O(1; x -> oo)\
"""
    ucode_str = \
"""\
O(1; x → ∞)\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = O(1/x, (x, oo))
    ascii_str = \
"""\
 /1         \\\n\
O|-; x -> oo|\n\
 \\x         /\
"""
    ucode_str = \
"""\
 ⎛1       ⎞\n\
O⎜─; x → ∞⎟\n\
 ⎝x       ⎠\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = O(x**2 + y**2, (x, oo), (y, oo))
    ascii_str = \
"""\
 / 2    2                    \\\n\
O\\x  + y ; (x, y) -> (oo, oo)/\
"""
    ucode_str = \
"""\
 ⎛ 2    2                 ⎞\n\
O⎝x  + y ; (x, y) → (∞, ∞)⎠\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

