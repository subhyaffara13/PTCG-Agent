
def test_int(doc):
    assert doc(m.get_int) == "get_int() -> int"


def test_int():
    a = Rational(5)
    assert int(a) == 5
    a = Rational(9, 10)
    assert int(a) == int(-a) == 0
    assert 1/(-1)**Rational(2, 3) == -(-1)**Rational(1, 3)
    # issue 10368
    a = Rational(32442016954, 78058255275)
    assert type(int(a)) is type(int(-a)) is int


def test_int(slice_test_df, slice_test_grouped, arg, expected_rows):
    # Test single integer
    result = slice_test_grouped._positional_selector[arg]
    expected = slice_test_df.iloc[expected_rows]

    tm.assert_frame_equal(result, expected)

