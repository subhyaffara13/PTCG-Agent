
def test_items(d, Asp):
    assert Asp.items() == d.items()


def test_items():
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})
    df_orig = df.copy()

    # Test this twice, since the second time, the item cache will be
    # triggered, and we want to make sure it still works then.
    for i in range(2):
        for name, ser in df.items():
            assert np.shares_memory(get_array(ser, name), get_array(df, name))

            # mutating df triggers a copy-on-write for that column / block
            ser.iloc[0] = 0

            assert not np.shares_memory(get_array(ser, name), get_array(df, name))
            tm.assert_frame_equal(df, df_orig)

