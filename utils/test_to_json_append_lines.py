
def test_to_json_append_lines():
    # GH 35849
    # Test ValueError when lines is not True
    df = DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    msg = (
        r"mode='a' \(append\) is only supported when "
        "lines is True and orient is 'records'"
    )
    with pytest.raises(ValueError, match=msg):
        df.to_json(mode="a", lines=False, orient="records")

