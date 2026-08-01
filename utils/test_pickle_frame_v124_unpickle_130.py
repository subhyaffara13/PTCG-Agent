
def test_pickle_frame_v124_unpickle_130(datapath):
    # GH#42345 DataFrame created in 1.2.x, unpickle in 1.3.x
    path = datapath(
        Path(__file__).parent,
        "data",
        "legacy_pickle",
        "1.2.4",
        "empty_frame_v1_2_4-GH#42345.pkl",
    )
    with open(path, "rb") as fd:
        df = pickle.load(fd)

    expected = DataFrame(index=[], columns=[])
    tm.assert_frame_equal(df, expected)

