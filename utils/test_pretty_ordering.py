
def test_pretty_ordering():
    assert pretty(x**2 + x + 1, order='lex') == \
"""\
 2        \n\
x  + x + 1\
"""
    assert pretty(x**2 + x + 1, order='rev-lex') == \
"""\
         2\n\
1 + x + x \
"""
    assert pretty(1 - x, order='lex') == '-x + 1'
    assert pretty(1 - x, order='rev-lex') == '1 - x'

    assert pretty(1 - 2*x, order='lex') == '-2*x + 1'
    assert pretty(1 - 2*x, order='rev-lex') == '1 - 2*x'

    f = 2*x**4 + y**2 - x**2 + y**3
    assert pretty(f, order=None) == \
"""\
   4    2    3    2\n\
2*x  - x  + y  + y \
"""
    assert pretty(f, order='lex') == \
"""\
   4    2    3    2\n\
2*x  - x  + y  + y \
"""
    assert pretty(f, order='rev-lex') == \
"""\
 2    3    2      4\n\
y  + y  - x  + 2*x \
"""

    expr = x - x**3/6 + x**5/120 + O(x**6)
    ascii_str = \
"""\
     3    5         \n\
    x    x      / 6\\\n\
x - -- + --- + O\\x /\n\
    6    120        \
"""
    ucode_str = \
"""\
     3    5         \n\
    x    x      ⎛ 6⎞\n\
x - ── + ─── + O⎝x ⎠\n\
    6    120        \
"""
    assert pretty(expr, order=None) == ascii_str
    assert upretty(expr, order=None) == ucode_str

    assert pretty(expr, order='lex') == ascii_str
    assert upretty(expr, order='lex') == ucode_str

    assert pretty(expr, order='rev-lex') == ascii_str
    assert upretty(expr, order='rev-lex') == ucode_str

