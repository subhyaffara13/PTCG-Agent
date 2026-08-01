
def test_s3_protocols(s3_bucket_public_with_data, s3so, tips_file, protocol):
    pytest.importorskip("s3fs")
    df_from_s3 = read_csv(
        f"{protocol}://{s3_bucket_public_with_data.name}/tips.csv",
        storage_options=s3so,
    )
    df_from_local = read_csv(tips_file)
    tm.assert_equal(df_from_s3, df_from_local)

