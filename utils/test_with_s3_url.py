
def test_with_s3_url(compression, s3_bucket_public, s3so, temp_file):
    # Bucket created in tests/io/conftest.py
    df = pd.read_json(StringIO('{"a": [1, 2, 3], "b": [4, 5, 6]}'))

    key = f"{uuid.uuid4()}.json"
    df.to_json(temp_file, compression=compression)
    with open(temp_file, "rb") as f:
        s3_bucket_public.put_object(Key=key, Body=f)

    roundtripped_df = pd.read_json(
        f"s3://{s3_bucket_public.name}/{key}",
        compression=compression,
        storage_options=s3so,
    )
    tm.assert_frame_equal(df, roundtripped_df)

