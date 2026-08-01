
def test_drop_duplicates_non_boolean_ignore_index(arg):
    # GH#38274
    df = DataFrame({"a": [1, 2, 1, 3]})
    msg = '^For argument "ignore_index" expected type bool, received type .*.$'
    with pytest.raises(ValueError, match=msg):
        df.drop_duplicates(ignore_index=arg)

