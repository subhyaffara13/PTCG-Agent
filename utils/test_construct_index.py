
def test_construct_index(all_data, dropna):
    # ensure that we do not coerce to different Index dtype or non-index

    all_data = all_data[:10]
    if dropna:
        other = np.array(all_data[~all_data.isna()])
    else:
        other = all_data

    result = pd.Index(pd.array(other, dtype=all_data.dtype))
    expected = pd.Index(other, dtype=all_data.dtype)
    assert all_data.dtype == expected.dtype  # dont coerce to object

    tm.assert_index_equal(result, expected)

