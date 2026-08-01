
def test_issctype(rep, expected):
    # ensure proper identification of scalar
    # data-types by issctype()
    actual = issctype(rep)
    assert type(actual) is bool
    assert_equal(actual, expected)

