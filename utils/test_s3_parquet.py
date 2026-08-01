
def test_s3_parquet(s3_bucket_public, s3so, df1):
    pytest.importorskip("fastparquet")
    pytest.importorskip("s3fs")

    fn = f"s3://{s3_bucket_public.name}/test.parquet"
    df1.to_parquet(
        fn, index=False, engine="fastparquet", compression=None, storage_options=s3so
    )
    df2 = read_parquet(fn, engine="fastparquet", storage_options=s3so)
    tm.assert_equal(df1, df2)

