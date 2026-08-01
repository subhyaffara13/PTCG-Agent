
def test_pretty_Lambda():
    # S.IdentityFunction is a special case
    expr = Lambda(y, y)
    assert pretty(expr) == "x -> x"
    assert upretty(expr) == "x ↦ x"

    expr = Lambda(x, x+1)
    assert pretty(expr) == "x -> x + 1"
    assert upretty(expr) == "x ↦ x + 1"

    expr = Lambda(x, x**2)
    ascii_str = \
"""\
      2\n\
x -> x \
"""
    ucode_str = \
"""\
     2\n\
x ↦ x \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Lambda(x, x**2)**2
    ascii_str = \
"""\
         2
/      2\\ \n\
\\x -> x / \
"""
    ucode_str = \
"""\
        2
⎛     2⎞ \n\
⎝x ↦ x ⎠ \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Lambda((x, y), x)
    ascii_str = "(x, y) -> x"
    ucode_str = "(x, y) ↦ x"
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Lambda((x, y), x**2)
    ascii_str = \
"""\
           2\n\
(x, y) -> x \
"""
    ucode_str = \
"""\
          2\n\
(x, y) ↦ x \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Lambda(((x, y),), x**2)
    ascii_str = \
"""\
              2\n\
((x, y),) -> x \
"""
    ucode_str = \
"""\
             2\n\
((x, y),) ↦ x \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

