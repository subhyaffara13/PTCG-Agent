
def test_ProductSet_prod_char_issue_10413():
    ascii_str = '[2, 3] x [4, 7]'
    ucode_str = '[2, 3] × [4, 7]'

    a, b = Interval(2, 3), Interval(4, 7)
    assert pretty(a*b) == ascii_str
    assert upretty(a*b) == ucode_str

