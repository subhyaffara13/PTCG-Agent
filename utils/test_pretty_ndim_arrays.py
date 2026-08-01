
def test_pretty_ndim_arrays():
    x, y, z, w = symbols("x y z w")

    for ArrayType in (ImmutableDenseNDimArray, ImmutableSparseNDimArray, MutableDenseNDimArray, MutableSparseNDimArray):
        # Basic: scalar array
        M = ArrayType(x)

        assert pretty(M) == "x"
        assert upretty(M) == "x"

        M = ArrayType([[1/x, y], [z, w]])
        M1 = ArrayType([1/x, y, z])

        M2 = tensorproduct(M1, M)
        M3 = tensorproduct(M, M)

        ascii_str = \
"""\
[1   ]\n\
[-  y]\n\
[x   ]\n\
[    ]\n\
[z  w]\
"""
        ucode_str = \
"""\
⎡1   ⎤\n\
⎢─  y⎥\n\
⎢x   ⎥\n\
⎢    ⎥\n\
⎣z  w⎦\
"""
        assert pretty(M) == ascii_str
        assert upretty(M) == ucode_str

        ascii_str = \
"""\
[1      ]\n\
[-  y  z]\n\
[x      ]\
"""
        ucode_str = \
"""\
⎡1      ⎤\n\
⎢─  y  z⎥\n\
⎣x      ⎦\
"""
        assert pretty(M1) == ascii_str
        assert upretty(M1) == ucode_str

        ascii_str = \
"""\
[[1   y]                       ]\n\
[[--  -]              [z      ]]\n\
[[ 2  x]  [ y    2 ]  [-   y*z]]\n\
[[x    ]  [ -   y  ]  [x      ]]\n\
[[     ]  [ x      ]  [       ]]\n\
[[z   w]  [        ]  [ 2     ]]\n\
[[-   -]  [y*z  w*y]  [z   w*z]]\n\
[[x   x]                       ]\
"""
        ucode_str = \
"""\
⎡⎡1   y⎤                       ⎤\n\
⎢⎢──  ─⎥              ⎡z      ⎤⎥\n\
⎢⎢ 2  x⎥  ⎡ y    2 ⎤  ⎢─   y⋅z⎥⎥\n\
⎢⎢x    ⎥  ⎢ ─   y  ⎥  ⎢x      ⎥⎥\n\
⎢⎢     ⎥  ⎢ x      ⎥  ⎢       ⎥⎥\n\
⎢⎢z   w⎥  ⎢        ⎥  ⎢ 2     ⎥⎥\n\
⎢⎢─   ─⎥  ⎣y⋅z  w⋅y⎦  ⎣z   w⋅z⎦⎥\n\
⎣⎣x   x⎦                       ⎦\
"""
        assert pretty(M2) == ascii_str
        assert upretty(M2) == ucode_str

        ascii_str = \
"""\
[ [1   y]             ]\n\
[ [--  -]             ]\n\
[ [ 2  x]   [ y    2 ]]\n\
[ [x    ]   [ -   y  ]]\n\
[ [     ]   [ x      ]]\n\
[ [z   w]   [        ]]\n\
[ [-   -]   [y*z  w*y]]\n\
[ [x   x]             ]\n\
[                     ]\n\
[[z      ]  [ w      ]]\n\
[[-   y*z]  [ -   w*y]]\n\
[[x      ]  [ x      ]]\n\
[[       ]  [        ]]\n\
[[ 2     ]  [      2 ]]\n\
[[z   w*z]  [w*z  w  ]]\
"""
        ucode_str = \
"""\
⎡ ⎡1   y⎤             ⎤\n\
⎢ ⎢──  ─⎥             ⎥\n\
⎢ ⎢ 2  x⎥   ⎡ y    2 ⎤⎥\n\
⎢ ⎢x    ⎥   ⎢ ─   y  ⎥⎥\n\
⎢ ⎢     ⎥   ⎢ x      ⎥⎥\n\
⎢ ⎢z   w⎥   ⎢        ⎥⎥\n\
⎢ ⎢─   ─⎥   ⎣y⋅z  w⋅y⎦⎥\n\
⎢ ⎣x   x⎦             ⎥\n\
⎢                     ⎥\n\
⎢⎡z      ⎤  ⎡ w      ⎤⎥\n\
⎢⎢─   y⋅z⎥  ⎢ ─   w⋅y⎥⎥\n\
⎢⎢x      ⎥  ⎢ x      ⎥⎥\n\
⎢⎢       ⎥  ⎢        ⎥⎥\n\
⎢⎢ 2     ⎥  ⎢      2 ⎥⎥\n\
⎣⎣z   w⋅z⎦  ⎣w⋅z  w  ⎦⎦\
"""
        assert pretty(M3) == ascii_str
        assert upretty(M3) == ucode_str

        Mrow = ArrayType([[x, y, 1 / z]])
        Mcolumn = ArrayType([[x], [y], [1 / z]])
        Mcol2 = ArrayType([Mcolumn.tolist()])

        ascii_str = \
"""\
[[      1]]\n\
[[x  y  -]]\n\
[[      z]]\
"""
        ucode_str = \
"""\
⎡⎡      1⎤⎤\n\
⎢⎢x  y  ─⎥⎥\n\
⎣⎣      z⎦⎦\
"""
        assert pretty(Mrow) == ascii_str
        assert upretty(Mrow) == ucode_str

        ascii_str = \
"""\
[x]\n\
[ ]\n\
[y]\n\
[ ]\n\
[1]\n\
[-]\n\
[z]\
"""
        ucode_str = \
"""\
⎡x⎤\n\
⎢ ⎥\n\
⎢y⎥\n\
⎢ ⎥\n\
⎢1⎥\n\
⎢─⎥\n\
⎣z⎦\
"""
        assert pretty(Mcolumn) == ascii_str
        assert upretty(Mcolumn) == ucode_str

        ascii_str = \
"""\
[[x]]\n\
[[ ]]\n\
[[y]]\n\
[[ ]]\n\
[[1]]\n\
[[-]]\n\
[[z]]\
"""
        ucode_str = \
"""\
⎡⎡x⎤⎤\n\
⎢⎢ ⎥⎥\n\
⎢⎢y⎥⎥\n\
⎢⎢ ⎥⎥\n\
⎢⎢1⎥⎥\n\
⎢⎢─⎥⎥\n\
⎣⎣z⎦⎦\
"""
        assert pretty(Mcol2) == ascii_str
        assert upretty(Mcol2) == ucode_str

