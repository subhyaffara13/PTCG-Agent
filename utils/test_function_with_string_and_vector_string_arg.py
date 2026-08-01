
def test_function_with_string_and_vector_string_arg():
    """Check if a string is NOT implicitly converted to a list, which was the
    behavior before fix of issue #1258"""
    assert m.func_with_string_or_vector_string_arg_overload(("A", "B")) == 2
    assert m.func_with_string_or_vector_string_arg_overload(["A", "B"]) == 2
    assert m.func_with_string_or_vector_string_arg_overload("A") == 3

