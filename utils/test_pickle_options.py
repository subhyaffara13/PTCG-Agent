
def test_pickle_options(fsspectest):
    df = DataFrame({"a": [0]})
    df.to_pickle("testmem://mockfile", storage_options={"test": "pickle_write"})
    assert fsspectest.test[0] == "pickle_write"
    out = read_pickle("testmem://mockfile", storage_options={"test": "pickle_read"})
    assert fsspectest.test[0] == "pickle_read"
    tm.assert_frame_equal(df, out)

