
def test_to_html_with_id():
    # GH 8496
    df = DataFrame({"A": [1, 2]}, index=Index(["a", "b"], name="myindexname"))
    result = df.to_html(index_names=False, table_id="TEST_ID")
    assert ' id="TEST_ID"' in result

