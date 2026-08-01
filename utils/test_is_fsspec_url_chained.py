
def test_is_fsspec_url_chained():
    # GH#48978 Support chained fsspec URLs
    # See https://filesystem-spec.readthedocs.io/en/latest/features.html#url-chaining.
    assert icom.is_fsspec_url("filecache::s3://pandas/test.csv")
    assert icom.is_fsspec_url("zip://test.csv::filecache::gcs://bucket/file.zip")
    assert icom.is_fsspec_url("filecache::zip://test.csv::gcs://bucket/file.zip")
    assert icom.is_fsspec_url("filecache::dask::s3://pandas/test.csv")
    assert not icom.is_fsspec_url("filecache:s3://pandas/test.csv")
    assert not icom.is_fsspec_url("filecache:::s3://pandas/test.csv")
    assert not icom.is_fsspec_url("filecache::://pandas/test.csv")

