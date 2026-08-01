
def test_mi_visit(code, expected, count_multi):
    code = dedent(code)
    expected = expected
    count_multi = count_multi
    assert mi_visit(code, count_multi) == expected

