
def test_strlines():
    q = 'this quote (") is in the middle'
    # the following assert rhs was prepared with
    # print(rawlines(strlines(q, 10)))
    assert strlines(q, 10) == dedent('''\
        (
        'this quo'
        'te (") i'
        's in the'
        ' middle'
        )''')
    assert q == (
        'this quo'
        'te (") i'
        's in the'
        ' middle'
        )
    q = "this quote (') is in the middle"
    assert strlines(q, 20) == dedent('''\
        (
        "this quote (') is "
        "in the middle"
        )''')
    assert strlines('\\left') == (
        '(\n'
        "r'\\left'\n"
        ')')
    assert strlines('\\left', short=True) == r"r'\left'"
    assert strlines('\\le"ft') == (
        '(\n'
        'r\'\\le"ft\'\n'
        ')')
    q = 'this\nother line'
    assert strlines(q) == rawlines(q)

