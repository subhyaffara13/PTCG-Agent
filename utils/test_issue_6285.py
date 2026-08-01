
def test_issue_6285():
    assert pretty(Pow(2, -5, evaluate=False)) == '1 \n--\n 5\n2 '
    assert pretty(Pow(x, (1/pi))) == \
    ' 1 \n'\
    ' --\n'\
    ' pi\n'\
    'x  '

