
def test_pretty_seq():
    expr = ()
    ascii_str = \
"""\
()\
"""
    ucode_str = \
"""\
()\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = []
    ascii_str = \
"""\
[]\
"""
    ucode_str = \
"""\
[]\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = {}
    expr_2 = {}
    ascii_str = \
"""\
{}\
"""
    ucode_str = \
"""\
{}\
"""
    assert pretty(expr) == ascii_str
    assert pretty(expr_2) == ascii_str
    assert upretty(expr) == ucode_str
    assert upretty(expr_2) == ucode_str

    expr = (1/x,)
    ascii_str = \
"""\
 1  \n\
(-,)\n\
 x  \
"""
    ucode_str = \
"""\
⎛1 ⎞\n\
⎜─,⎟\n\
⎝x ⎠\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = [x**2, 1/x, x, y, sin(th)**2/cos(ph)**2]
    ascii_str = \
"""\
                 2        \n\
  2  1        sin (theta) \n\
[x , -, x, y, -----------]\n\
     x            2       \n\
               cos (phi)  \
"""
    ucode_str = \
"""\
⎡                2   ⎤\n\
⎢ 2  1        sin (θ)⎥\n\
⎢x , ─, x, y, ───────⎥\n\
⎢    x           2   ⎥\n\
⎣             cos (φ)⎦\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = (x**2, 1/x, x, y, sin(th)**2/cos(ph)**2)
    ascii_str = \
"""\
                 2        \n\
  2  1        sin (theta) \n\
(x , -, x, y, -----------)\n\
     x            2       \n\
               cos (phi)  \
"""
    ucode_str = \
"""\
⎛                2   ⎞\n\
⎜ 2  1        sin (θ)⎟\n\
⎜x , ─, x, y, ───────⎟\n\
⎜    x           2   ⎟\n\
⎝             cos (φ)⎠\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Tuple(x**2, 1/x, x, y, sin(th)**2/cos(ph)**2)
    ascii_str = \
"""\
                 2        \n\
  2  1        sin (theta) \n\
(x , -, x, y, -----------)\n\
     x            2       \n\
               cos (phi)  \
"""
    ucode_str = \
"""\
⎛                2   ⎞\n\
⎜ 2  1        sin (θ)⎟\n\
⎜x , ─, x, y, ───────⎟\n\
⎜    x           2   ⎟\n\
⎝             cos (φ)⎠\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = {x: sin(x)}
    expr_2 = Dict({x: sin(x)})
    ascii_str = \
"""\
{x: sin(x)}\
"""
    ucode_str = \
"""\
{x: sin(x)}\
"""
    assert pretty(expr) == ascii_str
    assert pretty(expr_2) == ascii_str
    assert upretty(expr) == ucode_str
    assert upretty(expr_2) == ucode_str

    expr = {1/x: 1/y, x: sin(x)**2}
    expr_2 = Dict({1/x: 1/y, x: sin(x)**2})
    ascii_str = \
"""\
 1  1        2    \n\
{-: -, x: sin (x)}\n\
 x  y             \
"""
    ucode_str = \
"""\
⎧1  1        2   ⎫\n\
⎨─: ─, x: sin (x)⎬\n\
⎩x  y            ⎭\
"""
    assert pretty(expr) == ascii_str
    assert pretty(expr_2) == ascii_str
    assert upretty(expr) == ucode_str
    assert upretty(expr_2) == ucode_str

    # There used to be a bug with pretty-printing sequences of even height.
    expr = [x**2]
    ascii_str = \
"""\
  2 \n\
[x ]\
"""
    ucode_str = \
"""\
⎡ 2⎤\n\
⎣x ⎦\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = (x**2,)
    ascii_str = \
"""\
  2  \n\
(x ,)\
"""
    ucode_str = \
"""\
⎛ 2 ⎞\n\
⎝x ,⎠\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Tuple(x**2)
    ascii_str = \
"""\
  2  \n\
(x ,)\
"""
    ucode_str = \
"""\
⎛ 2 ⎞\n\
⎝x ,⎠\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = {x**2: 1}
    expr_2 = Dict({x**2: 1})
    ascii_str = \
"""\
  2    \n\
{x : 1}\
"""
    ucode_str = \
"""\
⎧ 2   ⎫\n\
⎨x : 1⎬\n\
⎩     ⎭\
"""
    assert pretty(expr) == ascii_str
    assert pretty(expr_2) == ascii_str
    assert upretty(expr) == ucode_str
    assert upretty(expr_2) == ucode_str

