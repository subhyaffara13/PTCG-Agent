
def test_non_fsspec_options():
    pytest.importorskip("pyarrow")
    with pytest.raises(ValueError, match="storage_options"):
        read_csv("localfile", storage_options={"a": True})
    with pytest.raises(ValueError, match="storage_options"):
        # separate test for parquet, which has a different code path
        read_parquet("localfile", storage_options={"a": True})
    by = io.BytesIO()

    with pytest.raises(ValueError, match="storage_options"):
        read_csv(by, storage_options={"a": True})

    df = DataFrame({"a": [0]})
    with pytest.raises(ValueError, match="storage_options"):
        df.to_parquet("nonfsspecpath", storage_options={"a": True})

