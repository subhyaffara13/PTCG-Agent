
def test_hash_tuples():
    tuples = [(1, "one"), (1, "two"), (2, "one")]
    result = hash_tuples(tuples)

    expected = hash_pandas_object(MultiIndex.from_tuples(tuples)).values
    tm.assert_numpy_array_equal(result, expected)

    # We only need to support MultiIndex and list-of-tuples
    msg = "|".join(["object is not iterable", "zip argument #1 must support iteration"])
    with pytest.raises(TypeError, match=msg):
        hash_tuples(tuples[0])

