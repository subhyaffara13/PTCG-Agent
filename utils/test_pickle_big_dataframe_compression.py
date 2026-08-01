
def test_pickle_big_dataframe_compression(protocol, compression, temp_file):
    # GH#39002
    df = DataFrame(range(100000))
    result = tm.round_trip_pathlib(
        partial(df.to_pickle, protocol=protocol, compression=compression),
        partial(pd.read_pickle, compression=compression),
        temp_file,
    )
    tm.assert_frame_equal(df, result)

