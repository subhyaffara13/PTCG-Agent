
def test_issue_4335():
    y = Function('y')
    expr = -y(x).diff(x)
    ucode_str = \
"""\
 d       \n\
-──(y(x))\n\
 dx      \
"""
    ascii_str = \
"""\
  d       \n\
- --(y(x))\n\
  dx      \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

