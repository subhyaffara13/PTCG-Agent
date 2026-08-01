
def test_pretty_UnevaluatedExpr():
    x = symbols('x')
    he = UnevaluatedExpr(1/x)

    ucode_str = \
"""\
1\n\
─\n\
x\
"""

    assert upretty(he) == ucode_str

    ucode_str = \
"""\
   2\n\
⎛1⎞ \n\
⎜─⎟ \n\
⎝x⎠ \
"""

    assert upretty(he**2) == ucode_str

    ucode_str = \
"""\
    1\n\
1 + ─\n\
    x\
"""

    assert upretty(he + 1) == ucode_str

    ucode_str = \
('''\
  1\n\
x⋅─\n\
  x\
''')
    assert upretty(x*he) == ucode_str

