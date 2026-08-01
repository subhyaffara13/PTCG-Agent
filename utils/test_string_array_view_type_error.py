
def test_string_array_view_type_error():
    arr = pd.array(["a", "b", "c"], dtype="string")
    with pytest.raises(TypeError, match="Cannot change data-type for string array."):
        arr.view("i8")

