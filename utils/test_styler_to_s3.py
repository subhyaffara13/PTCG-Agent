import uuid

def test_styler_to_s3(s3_bucket_public, s3so):
    # GH#46381
    mock_bucket_name = s3_bucket_public.name
    target_file = f"{uuid.uuid4()}.xlsx"
    df = DataFrame({"x": [1, 2, 3], "y": [2, 4, 6]})
    styler = df.style.set_sticky(axis="index")
    uri = f"s3://{mock_bucket_name}/{target_file}"
    styler.to_excel(uri, storage_options=s3so)
    result = read_excel(uri, index_col=0, storage_options=s3so)
    tm.assert_frame_equal(result, df)

