
def test_options_fp(df_compat, fp, temp_file):
    # use the set option

    with pd.option_context("io.parquet.engine", "fastparquet"):
        check_round_trip(df_compat, temp_file)

