
def test_read_table_options(fsspectest):
    # GH #39167
    df = DataFrame({"a": [0]})
    df.to_csv(
        "testmem://test/test.csv", storage_options={"test": "csv_write"}, index=False
    )
    assert fsspectest.test[0] == "csv_write"
    read_table("testmem://test/test.csv", storage_options={"test": "csv_read"})
    assert fsspectest.test[0] == "csv_read"

