
def test_pretty_limits():
    expr = Limit(x, x, oo)
    ascii_str = \
"""\
 lim x\n\
x->oo \
"""
    ucode_str = \
"""\
lim x\n\
x─→∞ \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Limit(x**2, x, 0)
    ascii_str = \
"""\
      2\n\
 lim x \n\
x->0+  \
"""
    ucode_str = \
"""\
      2\n\
 lim x \n\
x─→0⁺  \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Limit(1/x, x, 0)
    ascii_str = \
"""\
     1\n\
 lim -\n\
x->0+x\
"""
    ucode_str = \
"""\
     1\n\
 lim ─\n\
x─→0⁺x\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Limit(sin(x)/x, x, 0)
    ascii_str = \
"""\
     /sin(x)\\\n\
 lim |------|\n\
x->0+\\  x   /\
"""
    ucode_str = \
"""\
     ⎛sin(x)⎞\n\
 lim ⎜──────⎟\n\
x─→0⁺⎝  x   ⎠\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Limit(sin(x)/x, x, 0, "-")
    ascii_str = \
"""\
     /sin(x)\\\n\
 lim |------|\n\
x->0-\\  x   /\
"""
    ucode_str = \
"""\
     ⎛sin(x)⎞\n\
 lim ⎜──────⎟\n\
x─→0⁻⎝  x   ⎠\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Limit(x + sin(x), x, 0)
    ascii_str = \
"""\
 lim (x + sin(x))\n\
x->0+            \
"""
    ucode_str = \
"""\
 lim (x + sin(x))\n\
x─→0⁺            \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Limit(x, x, 0)**2
    ascii_str = \
"""\
        2\n\
/ lim x\\ \n\
\\x->0+ / \
"""
    ucode_str = \
"""\
        2\n\
⎛ lim x⎞ \n\
⎝x─→0⁺ ⎠ \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Limit(x*Limit(y/2,y,0), x, 0)
    ascii_str = \
"""\
     /       /y\\\\\n\
 lim |x* lim |-||\n\
x->0+\\  y->0+\\2//\
"""
    ucode_str = \
"""\
     ⎛       ⎛y⎞⎞\n\
 lim ⎜x⋅ lim ⎜─⎟⎟\n\
x─→0⁺⎝  y─→0⁺⎝2⎠⎠\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = 2*Limit(x*Limit(y/2,y,0), x, 0)
    ascii_str = \
"""\
       /       /y\\\\\n\
2* lim |x* lim |-||\n\
  x->0+\\  y->0+\\2//\
"""
    ucode_str = \
"""\
       ⎛       ⎛y⎞⎞\n\
2⋅ lim ⎜x⋅ lim ⎜─⎟⎟\n\
  x─→0⁺⎝  y─→0⁺⎝2⎠⎠\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Limit(sin(x), x, 0, dir='+-')
    ascii_str = \
"""\
lim sin(x)\n\
x->0      \
"""
    ucode_str = \
"""\
lim sin(x)\n\
x─→0      \
"""

    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

