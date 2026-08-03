from typing import Union

def test_pretty_Union_issue_10414():
    a, b = Interval(2, 3), Interval(4, 7)
    ucode_str = '[2, 3] ∪ [4, 7]'
    ascii_str = '[2, 3] U [4, 7]'
    assert upretty(Union(a, b)) == ucode_str
    assert pretty(Union(a, b)) == ascii_str

