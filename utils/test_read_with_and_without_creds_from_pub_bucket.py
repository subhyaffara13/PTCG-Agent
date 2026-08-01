
def test_read_with_and_without_creds_from_pub_bucket(
    s3_bucket_public_with_data, s3so, header
):
    # GH 34626
    pytest.importorskip("s3fs")
    nrows = 5
    df = read_csv(
        f"s3://{s3_bucket_public_with_data.name}/tips.csv",
        nrows=nrows,
        header=header,
        storage_options=s3so,
    )
    assert len(df) == nrows

