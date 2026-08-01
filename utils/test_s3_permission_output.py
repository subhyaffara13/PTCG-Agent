
def test_s3_permission_output(parser, s3_bucket_public, geom_df):
    s3fs = pytest.importorskip("s3fs")
    pytest.importorskip("lxml")

    with tm.external_error_raised((PermissionError, FileNotFoundError)):
        fs = s3fs.S3FileSystem(anon=True)
        fs.ls(s3_bucket_public.name)

        geom_df.to_xml(
            f"s3://{s3_bucket_public.name}/geom.xml", compression="zip", parser=parser
        )

