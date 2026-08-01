
def test_issue_17258():
    n = Symbol('n', integer=True)
    assert pretty(Sum(n, (n, -oo, 1))) == \
    '   1     \n'\
    '  __     \n'\
    '  \\ `    \n'\
    '   )    n\n'\
    '  /_,    \n'\
    'n = -oo  '

    assert upretty(Sum(n, (n, -oo, 1))) == \
"""\
  1     \n\
 ___    \n\
 ╲      \n\
  ╲     \n\
  ╱    n\n\
 ╱      \n\
 ‾‾‾    \n\
n = -∞  \
"""

