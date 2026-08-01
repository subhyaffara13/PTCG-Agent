
def test_pretty_Trace_issue_9044():
    X = Matrix([[1, 2], [3, 4]])
    Y = Matrix([[2, 4], [6, 8]])
    ascii_str_1 = \
"""\
  /[1  2]\\
tr|[    ]|
  \\[3  4]/\
"""
    ucode_str_1 = \
"""\
  ⎛⎡1  2⎤⎞
tr⎜⎢    ⎥⎟
  ⎝⎣3  4⎦⎠\
"""
    ascii_str_2 = \
"""\
  /[1  2]\\     /[2  4]\\
tr|[    ]| + tr|[    ]|
  \\[3  4]/     \\[6  8]/\
"""
    ucode_str_2 = \
"""\
  ⎛⎡1  2⎤⎞     ⎛⎡2  4⎤⎞
tr⎜⎢    ⎥⎟ + tr⎜⎢    ⎥⎟
  ⎝⎣3  4⎦⎠     ⎝⎣6  8⎦⎠\
"""
    assert pretty(Trace(X)) == ascii_str_1
    assert upretty(Trace(X)) == ucode_str_1

    assert pretty(Trace(X) + Trace(Y)) == ascii_str_2
    assert upretty(Trace(X) + Trace(Y)) == ucode_str_2

