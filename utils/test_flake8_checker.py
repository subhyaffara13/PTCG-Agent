
def test_flake8_checker():
    c = Flake8Checker(ast.parse(dedent(GENERAL_CASES[0][0])), 'test case')
    assert c.max_cc == -1
    assert c.no_assert is False
    assert list(c.run()) == []
    c.max_cc = 3
    assert list(c.run()) == [(7, 0, 'R701 \'f\' is too complex (4)', type(c))]

