
def test_issue_6324():
    x = Pow(2, 3, evaluate=False)
    y = Pow(10, -2, evaluate=False)
    e = Mul(x, y, evaluate=False)
    ucode_str = \
"""\
 3 \n\
2  \n\
───\n\
  2\n\
10 \
"""
    assert upretty(e) == ucode_str

