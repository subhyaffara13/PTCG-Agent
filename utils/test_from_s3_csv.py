
def test_from_s3_csv(s3_bucket_public_with_data, s3so, tips_file, compression_suffix):
    pytest.importorskip("s3fs")
    df_from_s3 = read_csv(
        f"s3://{s3_bucket_public_with_data.name}/tips.csv{compression_suffix}",
        storage_options=s3so,
    )
    df_from_local = read_csv(tips_file)
    tm.assert_equal(df_from_s3, df_from_local)

