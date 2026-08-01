
def test_maybe_unbox_numpy_scalar(typecode, using_python_scalars):
    # https://github.com/pandas-dev/pandas/pull/63016
    if typecode == "?":
        scalar = False
        expected = bool
    elif typecode in "bhilqnpBHILQNP":
        scalar = 0
        expected = int
    elif typecode in "efdg":
        scalar = 0.0
        expected = float
    elif typecode in "FDG":
        scalar = 0.0 + 0.0j
        expected = complex
    elif typecode in "SV":
        scalar = b""
        expected = bytes
    elif typecode == "U":
        scalar = ""
        expected = str
    elif typecode == "O":
        scalar = 0
        expected = int
    elif typecode == "M":
        scalar = datetime(2025, 1, 1)
        expected = Timestamp
    elif typecode == "m":
        scalar = timedelta(seconds=3)
        expected = Timedelta
    else:
        raise ValueError(f"typecode {typecode} not recognized")
    value = np.array([scalar], dtype=typecode)[0]
    result = maybe_unbox_numpy_scalar(value)
    if using_python_scalars:
        assert type(result) == expected
    else:
        assert result is value

