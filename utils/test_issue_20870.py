
def test_issue_20870():
    result = SOPform([a, b, c, d], [1, 2, 3, 4, 5, 6, 8, 9, 11, 12, 14, 15])
    expected = ((d & ~b) | (a & b & c) | (a & ~c & ~d) |
                (b & ~a & ~c) | (c & ~a & ~d))
    assert result == expected

