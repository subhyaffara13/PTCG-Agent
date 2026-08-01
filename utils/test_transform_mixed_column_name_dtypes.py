
def test_transform_mixed_column_name_dtypes():
    # GH39025
    df = DataFrame({"a": ["1"]})
    msg = r"Label\(s\) \[1, 'b'\] do not exist"
    with pytest.raises(KeyError, match=msg):
        df.transform({"a": int, 1: str, "b": int})

