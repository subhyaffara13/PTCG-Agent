
def test_elliptic_functions():
    ascii_str = \
"""\
 /  1  \\\n\
K|-----|\n\
 \\z + 1/\
"""
    ucode_str = \
"""\
 ⎛  1  ⎞\n\
K⎜─────⎟\n\
 ⎝z + 1⎠\
"""
    expr = elliptic_k(1/(z + 1))
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    ascii_str = \
"""\
 / |  1  \\\n\
F|1|-----|\n\
 \\ |z + 1/\
"""
    ucode_str = \
"""\
 ⎛ │  1  ⎞\n\
F⎜1│─────⎟\n\
 ⎝ │z + 1⎠\
"""
    expr = elliptic_f(1, 1/(1 + z))
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    ascii_str = \
"""\
 /  1  \\\n\
E|-----|\n\
 \\z + 1/\
"""
    ucode_str = \
"""\
 ⎛  1  ⎞\n\
E⎜─────⎟\n\
 ⎝z + 1⎠\
"""
    expr = elliptic_e(1/(z + 1))
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    ascii_str = \
"""\
 / |  1  \\\n\
E|1|-----|\n\
 \\ |z + 1/\
"""
    ucode_str = \
"""\
 ⎛ │  1  ⎞\n\
E⎜1│─────⎟\n\
 ⎝ │z + 1⎠\
"""
    expr = elliptic_e(1, 1/(1 + z))
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    ascii_str = \
"""\
  / |4\\\n\
Pi|3|-|\n\
  \\ |x/\
"""
    ucode_str = \
"""\
 ⎛ │4⎞\n\
Π⎜3│─⎟\n\
 ⎝ │x⎠\
"""
    expr = elliptic_pi(3, 4/x)
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    ascii_str = \
"""\
  /   4| \\\n\
Pi|3; -|6|\n\
  \\   x| /\
"""
    ucode_str = \
"""\
 ⎛   4│ ⎞\n\
Π⎜3; ─│6⎟\n\
 ⎝   x│ ⎠\
"""
    expr = elliptic_pi(3, 4/x, 6)
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

