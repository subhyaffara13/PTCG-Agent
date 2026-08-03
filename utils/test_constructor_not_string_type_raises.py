import re

def test_constructor_not_string_type_raises(array_lib, chunked):
    pa = pytest.importorskip("pyarrow")

    array_lib = pa if array_lib == "pyarrow" else np

    arr = array_lib.array([1, 2, 3])
    if chunked:
        if array_lib is np:
            pytest.skip("chunked not applicable to numpy array")
        arr = pa.chunked_array(arr)
    if array_lib is np:
        msg = "Unsupported type '<class 'numpy.ndarray'>' for ArrowExtensionArray"
    else:
        msg = re.escape(
            "ArrowStringArray requires a PyArrow (chunked) array of large_string type"
        )
    with pytest.raises(ValueError, match=msg):
        ArrowStringArray(arr)

