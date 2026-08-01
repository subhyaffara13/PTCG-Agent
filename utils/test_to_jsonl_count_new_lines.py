
def test_to_jsonl_count_new_lines():
    # GH36888
    df = DataFrame([[1, 2], [1, 2]], columns=["a", "b"])
    actual_new_lines_count = df.to_json(orient="records", lines=True).count("\n")
    expected_new_lines_count = 2
    assert actual_new_lines_count == expected_new_lines_count

