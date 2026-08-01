
def test_AugmentedAssignment():
    expr = AddAugmentedAssignment(x, y)
    ascii_str = \
"""\
x += y\
"""
    ucode_str = \
"""\
x += y\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = SubAugmentedAssignment(x, y)
    ascii_str = \
"""\
x -= y\
"""
    ucode_str = \
"""\
x -= y\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = MulAugmentedAssignment(x, y)
    ascii_str = \
"""\
x *= y\
"""
    ucode_str = \
"""\
x *= y\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = DivAugmentedAssignment(x, y)
    ascii_str = \
"""\
x /= y\
"""
    ucode_str = \
"""\
x /= y\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = ModAugmentedAssignment(x, y)
    ascii_str = \
"""\
x %= y\
"""
    ucode_str = \
"""\
x %= y\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

