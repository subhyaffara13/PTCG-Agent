
def test_issue_12675():
    x, y, t, j = symbols('x y t j')
    e = CoordSys3D('e')

    ucode_str = \
"""\
⎛   t⎞    \n\
⎜⎛x⎞ ⎟ j_e\n\
⎜⎜─⎟ ⎟    \n\
⎝⎝y⎠ ⎠    \
"""
    assert upretty((x/y)**t*e.j) == ucode_str
    ucode_str = \
"""\
⎛1⎞    \n\
⎜─⎟ j_e\n\
⎝y⎠    \
"""
    assert upretty((1/y)*e.j) == ucode_str

