
def test_issue_8344():
    from sympy.core import sympify
    e = sympify('2*x*y**2/1**2 + 1', evaluate=False)
    ucode_str = \
"""\
     2    \n\
2⋅x⋅y     \n\
────── + 1\n\
   2      \n\
  1       \
"""
    assert upretty(e) == ucode_str

