
def test_cross_engine_fp_pa(df_cross_compat, pa, fp, temp_file):
    # cross-compat with differing reading/writing engines
    df = df_cross_compat

    df.to_parquet(temp_file, engine=fp, compression=None)

    result = read_parquet(temp_file, engine=pa)
    tm.assert_frame_equal(result, df)

    result = read_parquet(temp_file, engine=pa, columns=["a", "d"])
    tm.assert_frame_equal(result, df[["a", "d"]])

