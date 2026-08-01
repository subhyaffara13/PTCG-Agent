
def test_issue_5767():
    assert set(solve([x**2 + y + 4], [x])) == \
        {(-sqrt(-y - 4),), (sqrt(-y - 4),)}

