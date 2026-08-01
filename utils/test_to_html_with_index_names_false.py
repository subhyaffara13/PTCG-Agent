
def test_to_html_with_index_names_false():
    # GH 16493
    df = DataFrame({"A": [1, 2]}, index=Index(["a", "b"], name="myindexname"))
    result = df.to_html(index_names=False)
    assert "myindexname" not in result

