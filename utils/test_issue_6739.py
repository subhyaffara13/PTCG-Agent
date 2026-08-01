
def test_issue_6739():
    ascii_str = \
"""\
  1  \n\
-----\n\
  ___\n\
\\/ x \
"""
    ucode_str = \
"""\
1 \n\
──\n\
√x\
"""
    assert pretty(1/sqrt(x)) == ascii_str
    assert upretty(1/sqrt(x)) == ucode_str

