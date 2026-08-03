import re

def test_arrow_string_addition_mixed_with_binary_raises(string_type):
    left = pd.Series(["a", None], dtype=ArrowDtype(string_type))
    right = pd.Series([b"b", b"c"], dtype=ArrowDtype(pa.binary()))

    msg = (
        f"operation 'add' not supported for dtype '{left.dtype}' "
        f"with dtype '{right.dtype}'"
    )
    with pytest.raises(TypeError, match=re.escape(msg)):
        left + right

    reflected_msg = (
        f"operation 'add' not supported for dtype '{right.dtype}' "
        f"with dtype '{left.dtype}'"
    )
    with pytest.raises(TypeError, match=re.escape(reflected_msg)):
        right + left

