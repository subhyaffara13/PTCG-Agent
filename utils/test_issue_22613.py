
def test_issue_22613():
    assert (0**(x - 2)).as_content_primitive() == (1, 0**(x - 2))
    assert (0**(x + 2)).as_content_primitive() == (1, 0**(x + 2))

