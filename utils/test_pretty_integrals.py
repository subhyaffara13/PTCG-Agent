
def test_pretty_integrals():
    expr = Integral(log(x), x)
    ascii_str = \
"""\
  /         \n\
 |          \n\
 | log(x) dx\n\
 |          \n\
/           \
"""
    ucode_str = \
"""\
⌠          \n\
⎮ log(x) dx\n\
⌡          \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Integral(x**2, x)
    ascii_str = \
"""\
  /     \n\
 |      \n\
 |  2   \n\
 | x  dx\n\
 |      \n\
/       \
"""
    ucode_str = \
"""\
⌠      \n\
⎮  2   \n\
⎮ x  dx\n\
⌡      \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Integral((sin(x))**2 / (tan(x))**2)
    ascii_str = \
"""\
  /          \n\
 |           \n\
 |    2      \n\
 | sin (x)   \n\
 | ------- dx\n\
 |    2      \n\
 | tan (x)   \n\
 |           \n\
/            \
"""
    ucode_str = \
"""\
⌠           \n\
⎮    2      \n\
⎮ sin (x)   \n\
⎮ ─────── dx\n\
⎮    2      \n\
⎮ tan (x)   \n\
⌡           \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Integral(x**(2**x), x)
    ascii_str = \
"""\
  /        \n\
 |         \n\
 |  / x\\   \n\
 |  \\2 /   \n\
 | x     dx\n\
 |         \n\
/          \
"""
    ucode_str = \
"""\
⌠         \n\
⎮  ⎛ x⎞   \n\
⎮  ⎝2 ⎠   \n\
⎮ x     dx\n\
⌡         \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Integral(x**2, (x, 1, 2))
    ascii_str = \
"""\
  2      \n\
  /      \n\
 |       \n\
 |   2   \n\
 |  x  dx\n\
 |       \n\
/        \n\
1        \
"""
    ucode_str = \
"""\
2      \n\
⌠      \n\
⎮  2   \n\
⎮ x  dx\n\
⌡      \n\
1      \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Integral(x**2, (x, Rational(1, 2), 10))
    ascii_str = \
"""\
 10      \n\
  /      \n\
 |       \n\
 |   2   \n\
 |  x  dx\n\
 |       \n\
/        \n\
1/2      \
"""
    ucode_str = \
"""\
10       \n\
⌠        \n\
⎮    2   \n\
⎮   x  dx\n\
⌡        \n\
1/2      \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Integral(x**2*y**2, x, y)
    ascii_str = \
"""\
  /  /           \n\
 |  |            \n\
 |  |  2  2      \n\
 |  | x *y  dx dy\n\
 |  |            \n\
/  /             \
"""
    ucode_str = \
"""\
⌠ ⌠            \n\
⎮ ⎮  2  2      \n\
⎮ ⎮ x ⋅y  dx dy\n\
⌡ ⌡            \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Integral(sin(th)/cos(ph), (th, 0, pi), (ph, 0, 2*pi))
    ascii_str = \
"""\
 2*pi pi                           \n\
   /   /                           \n\
  |   |                            \n\
  |   |  sin(theta)                \n\
  |   |  ---------- d(theta) d(phi)\n\
  |   |   cos(phi)                 \n\
  |   |                            \n\
 /   /                             \n\
0    0                             \
"""
    ucode_str = \
"""\
2⋅π π             \n\
 ⌠  ⌠             \n\
 ⎮  ⎮ sin(θ)      \n\
 ⎮  ⎮ ────── dθ dφ\n\
 ⎮  ⎮ cos(φ)      \n\
 ⌡  ⌡             \n\
 0  0             \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

