
def test_issue_6082():
    # Comparison is symmetric
    assert Basic.compare(Max(x, 1), Max(x, 2)) == \
      - Basic.compare(Max(x, 2), Max(x, 1))
    # Equal expressions compare equal
    assert Basic.compare(Max(x, 1), Max(x, 1)) == 0
    # Basic subtypes (such as Max) compare different than standard types
    assert Basic.compare(Max(1, x), frozenset((1, x))) != 0

