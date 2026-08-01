
def test_pretty_sqrt():
    expr = sqrt(2)
    ascii_str = \
"""\
  ___\n\
\\/ 2 \
"""
    ucode_str = \
"√2"
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = 2**Rational(1, 3)
    ascii_str = \
"""\
3 ___\n\
\\/ 2 \
"""
    ucode_str = \
"""\
3 ___\n\
╲╱ 2 \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = 2**Rational(1, 1000)
    ascii_str = \
"""\
1000___\n\
  \\/ 2 \
"""
    ucode_str = \
"""\
1000___\n\
  ╲╱ 2 \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = sqrt(x**2 + 1)
    ascii_str = \
"""\
   ________\n\
  /  2     \n\
\\/  x  + 1 \
"""
    ucode_str = \
"""\
   ________\n\
  ╱  2     \n\
╲╱  x  + 1 \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = (1 + sqrt(5))**Rational(1, 3)
    ascii_str = \
"""\
   ___________\n\
3 /       ___ \n\
\\/  1 + \\/ 5  \
"""
    ucode_str = \
"""\
3 ________\n\
╲╱ 1 + √5 \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = 2**(1/x)
    ascii_str = \
"""\
x ___\n\
\\/ 2 \
"""
    ucode_str = \
"""\
x ___\n\
╲╱ 2 \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = sqrt(2 + pi)
    ascii_str = \
"""\
  ________\n\
\\/ 2 + pi \
"""
    ucode_str = \
"""\
  _______\n\
╲╱ 2 + π \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = (2 + (
        1 + x**2)/(2 + x))**Rational(1, 4) + (1 + x**Rational(1, 1000))/sqrt(3 + x**2)
    ascii_str = \
"""\
     ____________              \n\
    /      2        1000___    \n\
   /      x  + 1      \\/ x  + 1\n\
4 /   2 + ------  + -----------\n\
\\/        x + 2        ________\n\
                      /  2     \n\
                    \\/  x  + 3 \
"""
    ucode_str = \
"""\
     ____________              \n\
    ╱      2        1000___    \n\
   ╱      x  + 1      ╲╱ x  + 1\n\
4 ╱   2 + ──────  + ───────────\n\
╲╱        x + 2        ________\n\
                      ╱  2     \n\
                    ╲╱  x  + 3 \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

