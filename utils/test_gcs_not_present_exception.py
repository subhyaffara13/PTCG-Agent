
def test_gcs_not_present_exception():
    with tm.external_error_raised(ImportError):
        read_csv("gs://test/test.csv")

