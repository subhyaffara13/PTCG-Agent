
def test_issue_14411():
    assert limit(3*sec(4*pi*x - x/3), x, 3*pi/(24*pi - 2)) is -oo

