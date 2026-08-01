
def test_is_fsspec_url():
    assert icom.is_fsspec_url("gcs://pandas/somethingelse.com")
    assert icom.is_fsspec_url("gs://pandas/somethingelse.com")
    # the following is the only remote URL that is handled without fsspec
    assert not icom.is_fsspec_url("http://pandas/somethingelse.com")
    assert not icom.is_fsspec_url("random:pandas/somethingelse.com")
    assert not icom.is_fsspec_url("/local/path")
    assert not icom.is_fsspec_url("relative/local/path")
    # fsspec URL in string should not be recognized
    assert not icom.is_fsspec_url("this is not fsspec://url")
    assert not icom.is_fsspec_url("{'url': 'gs://pandas/somethingelse.com'}")
    # accept everything that conforms to RFC 3986 schema
    assert icom.is_fsspec_url("RFC-3986+compliant.spec://something")

