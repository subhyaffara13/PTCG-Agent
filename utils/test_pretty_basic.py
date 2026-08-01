
def test_pretty_basic():
    assert pretty( -Rational(1)/2 ) == '-1/2'
    assert pretty( -Rational(13)/22 ) == \
"""\
-13 \n\
----\n\
 22 \
"""
    expr = oo
    ascii_str = \
"""\
oo\
"""
    ucode_str = \
"""\
∞\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = (x**2)
    ascii_str = \
"""\
 2\n\
x \
"""
    ucode_str = \
"""\
 2\n\
x \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = 1/x
    ascii_str = \
"""\
1\n\
-\n\
x\
"""
    ucode_str = \
"""\
1\n\
─\n\
x\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    # not the same as 1/x
    expr = x**-1.0
    ascii_str = \
"""\
 -1.0\n\
x    \
"""
    ucode_str = \
"""\
 -1.0\n\
x    \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    # see issue #2860
    expr = Pow(S(2), -1.0, evaluate=False)
    ascii_str = \
"""\
 -1.0\n\
2    \
"""
    ucode_str = \
"""\
 -1.0\n\
2    \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = y*x**-2
    ascii_str = \
"""\
y \n\
--\n\
 2\n\
x \
"""
    ucode_str = \
"""\
y \n\
──\n\
 2\n\
x \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    #see issue #14033
    expr = x**Rational(1, 3)
    ascii_str = \
"""\
 1/3\n\
x   \
"""
    ucode_str = \
"""\
 1/3\n\
x   \
"""
    assert xpretty(expr, use_unicode=False, wrap_line=False,\
    root_notation = False) == ascii_str
    assert xpretty(expr, use_unicode=True, wrap_line=False,\
    root_notation = False) == ucode_str

    expr = x**Rational(-5, 2)
    ascii_str = \
"""\
 1  \n\
----\n\
 5/2\n\
x   \
"""
    ucode_str = \
"""\
 1  \n\
────\n\
 5/2\n\
x   \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = (-2)**x
    ascii_str = \
"""\
    x\n\
(-2) \
"""
    ucode_str = \
"""\
    x\n\
(-2) \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    # See issue 4923
    expr = Pow(3, 1, evaluate=False)
    ascii_str = \
"""\
 1\n\
3 \
"""
    ucode_str = \
"""\
 1\n\
3 \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = (x**2 + x + 1)
    ascii_str_1 = \
"""\
         2\n\
1 + x + x \
"""
    ascii_str_2 = \
"""\
 2        \n\
x  + x + 1\
"""
    ascii_str_3 = \
"""\
 2        \n\
x  + 1 + x\
"""
    ucode_str_1 = \
"""\
         2\n\
1 + x + x \
"""
    ucode_str_2 = \
"""\
 2        \n\
x  + x + 1\
"""
    ucode_str_3 = \
"""\
 2        \n\
x  + 1 + x\
"""
    assert pretty(expr) in [ascii_str_1, ascii_str_2, ascii_str_3]
    assert upretty(expr) in [ucode_str_1, ucode_str_2, ucode_str_3]

    expr = 1 - x
    ascii_str_1 = \
"""\
1 - x\
"""
    ascii_str_2 = \
"""\
-x + 1\
"""
    ucode_str_1 = \
"""\
1 - x\
"""
    ucode_str_2 = \
"""\
-x + 1\
"""
    assert pretty(expr) in [ascii_str_1, ascii_str_2]
    assert upretty(expr) in [ucode_str_1, ucode_str_2]

    expr = 1 - 2*x
    ascii_str_1 = \
"""\
1 - 2*x\
"""
    ascii_str_2 = \
"""\
-2*x + 1\
"""
    ucode_str_1 = \
"""\
1 - 2⋅x\
"""
    ucode_str_2 = \
"""\
-2⋅x + 1\
"""
    assert pretty(expr) in [ascii_str_1, ascii_str_2]
    assert upretty(expr) in [ucode_str_1, ucode_str_2]

    expr = x/y
    ascii_str = \
"""\
x\n\
-\n\
y\
"""
    ucode_str = \
"""\
x\n\
─\n\
y\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = -x/y
    ascii_str = \
"""\
-x \n\
---\n\
 y \
"""
    ucode_str = \
"""\
-x \n\
───\n\
 y \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = (x + 2)/y
    ascii_str_1 = \
"""\
2 + x\n\
-----\n\
  y  \
"""
    ascii_str_2 = \
"""\
x + 2\n\
-----\n\
  y  \
"""
    ucode_str_1 = \
"""\
2 + x\n\
─────\n\
  y  \
"""
    ucode_str_2 = \
"""\
x + 2\n\
─────\n\
  y  \
"""
    assert pretty(expr) in [ascii_str_1, ascii_str_2]
    assert upretty(expr) in [ucode_str_1, ucode_str_2]

    expr = (1 + x)*y
    ascii_str_1 = \
"""\
y*(1 + x)\
"""
    ascii_str_2 = \
"""\
(1 + x)*y\
"""
    ascii_str_3 = \
"""\
y*(x + 1)\
"""
    ucode_str_1 = \
"""\
y⋅(1 + x)\
"""
    ucode_str_2 = \
"""\
(1 + x)⋅y\
"""
    ucode_str_3 = \
"""\
y⋅(x + 1)\
"""
    assert pretty(expr) in [ascii_str_1, ascii_str_2, ascii_str_3]
    assert upretty(expr) in [ucode_str_1, ucode_str_2, ucode_str_3]

    # Test for correct placement of the negative sign
    expr = -5*x/(x + 10)
    ascii_str_1 = \
"""\
-5*x  \n\
------\n\
10 + x\
"""
    ascii_str_2 = \
"""\
-5*x  \n\
------\n\
x + 10\
"""
    ucode_str_1 = \
"""\
-5⋅x  \n\
──────\n\
10 + x\
"""
    ucode_str_2 = \
"""\
-5⋅x  \n\
──────\n\
x + 10\
"""
    assert pretty(expr) in [ascii_str_1, ascii_str_2]
    assert upretty(expr) in [ucode_str_1, ucode_str_2]

    expr = -S.Half - 3*x
    ascii_str = \
"""\
-3*x - 1/2\
"""
    ucode_str = \
"""\
-3⋅x - 1/2\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = S.Half - 3*x
    ascii_str = \
"""\
1/2 - 3*x\
"""
    ucode_str = \
"""\
1/2 - 3⋅x\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = -S.Half - 3*x/2
    ascii_str = \
"""\
  3*x   1\n\
- --- - -\n\
   2    2\
"""
    ucode_str = \
"""\
  3⋅x   1\n\
- ─── - ─\n\
   2    2\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = S.Half - 3*x/2
    ascii_str = \
"""\
1   3*x\n\
- - ---\n\
2    2 \
"""
    ucode_str = \
"""\
1   3⋅x\n\
─ - ───\n\
2    2 \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

