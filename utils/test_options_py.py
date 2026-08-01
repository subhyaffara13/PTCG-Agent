
def test_options_py(df_compat, pa, using_infer_string, temp_file):
    # use the set option
    if using_infer_string and not pa_version_under19p0:
        df_compat.columns = df_compat.columns.astype("str")

    with pd.option_context("io.parquet.engine", "pyarrow"):
        check_round_trip(df_compat, temp_file)

