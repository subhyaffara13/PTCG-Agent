
def test_rpow_one_to_na():
    # https://github.com/pandas-dev/pandas/issues/22022
    # https://github.com/pandas-dev/pandas/issues/29997
    arr = pd.array([pd.NA, pd.NA], dtype="Float64")
    result = np.array([1.0, 2.0]) ** arr
    expected = pd.array([1.0, pd.NA], dtype="Float64")
    tm.assert_extension_array_equal(result, expected)


def test_rpow_one_to_na():
    # https://github.com/pandas-dev/pandas/issues/22022
    # https://github.com/pandas-dev/pandas/issues/29997
    arr = pd.array([pd.NA, pd.NA], dtype="Int64")
    result = np.array([1.0, 2.0]) ** arr
    expected = pd.array([1.0, pd.NA], dtype="Float64")
    tm.assert_extension_array_equal(result, expected)

