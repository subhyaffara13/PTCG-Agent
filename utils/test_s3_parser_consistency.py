
def test_s3_parser_consistency(s3_bucket_public_with_data, s3so):
    pytest.importorskip("s3fs")
    pytest.importorskip("lxml")
    s3 = f"s3://{s3_bucket_public_with_data.name}/books.xml"
    df_lxml = read_xml(s3, parser="lxml", storage_options=s3so)

    df_etree = read_xml(s3, parser="etree", storage_options=s3so)

    tm.assert_frame_equal(df_lxml, df_etree)

