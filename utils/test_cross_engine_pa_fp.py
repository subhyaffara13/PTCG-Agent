
def test_cross_engine_pa_fp(df_cross_compat, pa, fp, temp_file):
    # cross-compat with differing reading/writing engines

    df = df_cross_compat
    df.to_parquet(temp_file, engine=pa, compression=None)

    result = read_parquet(temp_file, engine=fp)
    tm.assert_frame_equal(result, df)

    result = read_parquet(temp_file, engine=fp, columns=["a", "d"])
    tm.assert_frame_equal(result, df[["a", "d"]])

