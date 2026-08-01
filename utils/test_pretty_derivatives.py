
def test_pretty_derivatives():
    # Simple
    expr = Derivative(log(x), x, evaluate=False)
    ascii_str = \
"""\
d         \n\
--(log(x))\n\
dx        \
"""
    ucode_str = \
"""\
d         \n\
──(log(x))\n\
dx        \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Derivative(log(x), x, evaluate=False) + x
    ascii_str_1 = \
"""\
    d         \n\
x + --(log(x))\n\
    dx        \
"""
    ascii_str_2 = \
"""\
d             \n\
--(log(x)) + x\n\
dx            \
"""
    ucode_str_1 = \
"""\
    d         \n\
x + ──(log(x))\n\
    dx        \
"""
    ucode_str_2 = \
"""\
d             \n\
──(log(x)) + x\n\
dx            \
"""
    assert pretty(expr) in [ascii_str_1, ascii_str_2]
    assert upretty(expr) in [ucode_str_1, ucode_str_2]

    # basic partial derivatives
    expr = Derivative(log(x + y) + x, x)
    ascii_str_1 = \
"""\
d                 \n\
--(log(x + y) + x)\n\
dx                \
"""
    ascii_str_2 = \
"""\
d                 \n\
--(x + log(x + y))\n\
dx                \
"""
    ucode_str_1 = \
"""\
∂                 \n\
──(log(x + y) + x)\n\
∂x                \
"""
    ucode_str_2 = \
"""\
∂                 \n\
──(x + log(x + y))\n\
∂x                \
"""
    assert pretty(expr) in [ascii_str_1, ascii_str_2]
    assert upretty(expr) in [ucode_str_1, ucode_str_2], upretty(expr)

    # Multiple symbols
    expr = Derivative(log(x) + x**2, x, y)
    ascii_str_1 = \
"""\
   2              \n\
  d  /          2\\\n\
-----\\log(x) + x /\n\
dy dx             \
"""
    ascii_str_2 = \
"""\
   2              \n\
  d  / 2         \\\n\
-----\\x  + log(x)/\n\
dy dx             \
"""
    ascii_str_3 = \
"""\
  2               \n\
 d   / 2         \\\n\
-----\\x  + log(x)/\n\
dy dx             \
"""
    ucode_str_1 = \
"""\
   2              \n\
  d  ⎛          2⎞\n\
─────⎝log(x) + x ⎠\n\
dy dx             \
"""
    ucode_str_2 = \
"""\
   2              \n\
  d  ⎛ 2         ⎞\n\
─────⎝x  + log(x)⎠\n\
dy dx             \
"""
    ucode_str_3 = \
"""\
  2               \n\
 d   ⎛ 2         ⎞\n\
─────⎝x  + log(x)⎠\n\
dy dx             \
"""
    assert pretty(expr) in [ascii_str_1, ascii_str_2, ascii_str_3]
    assert upretty(expr) in [ucode_str_1, ucode_str_2, ucode_str_3]

    expr = Derivative(2*x*y, y, x) + x**2
    ascii_str_1 = \
"""\
   2             \n\
  d             2\n\
-----(2*x*y) + x \n\
dx dy            \
"""
    ascii_str_2 = \
"""\
        2        \n\
 2     d         \n\
x  + -----(2*x*y)\n\
     dx dy       \
"""
    ascii_str_3 = \
"""\
       2         \n\
 2    d          \n\
x  + -----(2*x*y)\n\
     dx dy       \
"""
    ucode_str_1 = \
"""\
   2             \n\
  ∂             2\n\
─────(2⋅x⋅y) + x \n\
∂x ∂y            \
"""
    ucode_str_2 = \
"""\
        2        \n\
 2     ∂         \n\
x  + ─────(2⋅x⋅y)\n\
     ∂x ∂y       \
"""
    ucode_str_3 = \
"""\
       2         \n\
 2    ∂          \n\
x  + ─────(2⋅x⋅y)\n\
     ∂x ∂y       \
"""
    assert pretty(expr) in [ascii_str_1, ascii_str_2, ascii_str_3]
    assert upretty(expr) in [ucode_str_1, ucode_str_2, ucode_str_3]

    expr = Derivative(2*x*y, x, x)
    ascii_str = \
"""\
 2        \n\
d         \n\
---(2*x*y)\n\
  2       \n\
dx        \
"""
    ucode_str = \
"""\
 2        \n\
∂         \n\
───(2⋅x⋅y)\n\
  2       \n\
∂x        \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Derivative(2*x*y, x, 17)
    ascii_str = \
"""\
 17        \n\
d          \n\
----(2*x*y)\n\
  17       \n\
dx         \
"""
    ucode_str = \
"""\
 17        \n\
∂          \n\
────(2⋅x⋅y)\n\
  17       \n\
∂x         \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Derivative(2*x*y, x, x, y)
    ascii_str = \
"""\
   3         \n\
  d          \n\
------(2*x*y)\n\
     2       \n\
dy dx        \
"""
    ucode_str = \
"""\
   3         \n\
  ∂          \n\
──────(2⋅x⋅y)\n\
     2       \n\
∂y ∂x        \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    # Greek letters
    alpha = Symbol('alpha')
    beta = Function('beta')
    expr = beta(alpha).diff(alpha)
    ascii_str = \
"""\
  d                \n\
------(beta(alpha))\n\
dalpha             \
"""
    ucode_str = \
"""\
d       \n\
──(β(α))\n\
dα      \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Derivative(f(x), (x, n))

    ascii_str = \
"""\
 n       \n\
d        \n\
---(f(x))\n\
  n      \n\
dx       \
"""
    ucode_str = \
"""\
 n       \n\
d        \n\
───(f(x))\n\
  n      \n\
dx       \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

