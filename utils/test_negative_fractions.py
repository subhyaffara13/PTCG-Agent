
def test_negative_fractions():
    expr = -x/y
    ascii_str =\
"""\
-x \n\
---\n\
 y \
"""
    ucode_str =\
"""\
-x \n\
───\n\
 y \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str
    expr = -x*z/y
    ascii_str =\
"""\
-x*z \n\
-----\n\
  y  \
"""
    ucode_str =\
"""\
-x⋅z \n\
─────\n\
  y  \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str
    expr = x**2/y
    ascii_str =\
"""\
 2\n\
x \n\
--\n\
y \
"""
    ucode_str =\
"""\
 2\n\
x \n\
──\n\
y \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str
    expr = -x**2/y
    ascii_str =\
"""\
  2 \n\
-x  \n\
----\n\
 y  \
"""
    ucode_str =\
"""\
  2 \n\
-x  \n\
────\n\
 y  \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str
    expr = -x/(y*z)
    ascii_str =\
"""\
-x \n\
---\n\
y*z\
"""
    ucode_str =\
"""\
-x \n\
───\n\
y⋅z\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str
    expr = -a/y**2
    ascii_str =\
"""\
-a \n\
---\n\
 2 \n\
y  \
"""
    ucode_str =\
"""\
-a \n\
───\n\
 2 \n\
y  \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str
    expr = y**(-a/b)
    ascii_str =\
"""\
 -a \n\
 ---\n\
  b \n\
y   \
"""
    ucode_str =\
"""\
 -a \n\
 ───\n\
  b \n\
y   \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str
    expr = -1/y**2
    ascii_str =\
"""\
-1 \n\
---\n\
 2 \n\
y  \
"""
    ucode_str =\
"""\
-1 \n\
───\n\
 2 \n\
y  \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str
    expr = -10/b**2
    ascii_str =\
"""\
-10 \n\
----\n\
  2 \n\
 b  \
"""
    ucode_str =\
"""\
-10 \n\
────\n\
  2 \n\
 b  \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str
    expr = Rational(-200, 37)
    ascii_str =\
"""\
-200 \n\
-----\n\
 37  \
"""
    ucode_str =\
"""\
-200 \n\
─────\n\
 37  \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

