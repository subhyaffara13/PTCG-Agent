
def test_pretty_matrix():
    # Empty Matrix
    expr = Matrix()
    ascii_str = "[]"
    unicode_str = "[]"
    assert pretty(expr) == ascii_str
    assert upretty(expr) == unicode_str
    expr = Matrix(2, 0, lambda i, j: 0)
    ascii_str = "[]"
    unicode_str = "[]"
    assert pretty(expr) == ascii_str
    assert upretty(expr) == unicode_str
    expr = Matrix(0, 2, lambda i, j: 0)
    ascii_str = "[]"
    unicode_str = "[]"
    assert pretty(expr) == ascii_str
    assert upretty(expr) == unicode_str
    expr = Matrix([[x**2 + 1, 1], [y, x + y]])
    ascii_str_1 = \
"""\
[     2       ]
[1 + x     1  ]
[             ]
[  y     x + y]\
"""
    ascii_str_2 = \
"""\
[ 2           ]
[x  + 1    1  ]
[             ]
[  y     x + y]\
"""
    ucode_str_1 = \
"""\
⎡     2       ⎤
⎢1 + x     1  ⎥
⎢             ⎥
⎣  y     x + y⎦\
"""
    ucode_str_2 = \
"""\
⎡ 2           ⎤
⎢x  + 1    1  ⎥
⎢             ⎥
⎣  y     x + y⎦\
"""
    assert pretty(expr) in [ascii_str_1, ascii_str_2]
    assert upretty(expr) in [ucode_str_1, ucode_str_2]

    expr = Matrix([[x/y, y, th], [0, exp(I*k*ph), 1]])
    ascii_str = \
"""\
[x                 ]
[-     y      theta]
[y                 ]
[                  ]
[    I*k*phi       ]
[0  e           1  ]\
"""
    ucode_str = \
"""\
⎡x           ⎤
⎢─    y     θ⎥
⎢y           ⎥
⎢            ⎥
⎢    ⅈ⋅k⋅φ   ⎥
⎣0  ℯ       1⎦\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    unicode_str = \
"""\
⎡v̇_msc_00     0         0    ⎤
⎢                            ⎥
⎢   0      v̇_msc_01     0    ⎥
⎢                            ⎥
⎣   0         0      v̇_msc_02⎦\
"""

    expr = diag(*MatrixSymbol('vdot_msc',1,3))
    assert upretty(expr) == unicode_str

