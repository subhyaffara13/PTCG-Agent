import sys

def test_string_too_large_error():
    arr = np.array(["a", "b", "c"], dtype=StringDType())
    with pytest.raises(OverflowError):
        arr * (sys.maxsize + 1)

