
def test_rawlines():
    assert rawlines('a a\na') == "dedent('''\\\n    a a\n    a''')"
    assert rawlines('a a') == "'a a'"
    assert rawlines(strlines('\\le"ft')) == (
        '(\n'
        "    '(\\n'\n"
        '    \'r\\\'\\\\le"ft\\\'\\n\'\n'
        "    ')'\n"
        ')')

