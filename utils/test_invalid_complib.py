
def test_invalid_complib(temp_h5_path):
    df = DataFrame(
        np.random.default_rng(2).random((4, 5)),
        index=list("abcd"),
        columns=list("ABCDE"),
    )
    msg = r"complib only supports \[.*\] compression."
    with pytest.raises(ValueError, match=msg):
        df.to_hdf(temp_h5_path, key="df", complib="foolib")

