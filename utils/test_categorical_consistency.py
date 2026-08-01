
def test_categorical_consistency(s1, categorize):
    # see gh-15143
    #
    # Check that categoricals hash consistent with their values,
    # not codes. This should work for categoricals of any dtype.
    s1 = Series(s1)
    s2 = s1.astype("category").cat.set_categories(s1)
    s3 = s2.cat.set_categories(list(reversed(s1)))

    # These should all hash identically.
    h1 = hash_pandas_object(s1, categorize=categorize)
    h2 = hash_pandas_object(s2, categorize=categorize)
    h3 = hash_pandas_object(s3, categorize=categorize)

    tm.assert_series_equal(h1, h2)
    tm.assert_series_equal(h1, h3)

