
def test_invalid_dtype_backend(temp_file):
    msg = (
        "dtype_backend numpy is invalid, only 'numpy_nullable' and "
        "'pyarrow' are allowed."
    )
    df = pd.DataFrame({"int": list(range(1, 4))})
    df.to_orc(temp_file)
    with pytest.raises(ValueError, match=msg):
        read_orc(temp_file, dtype_backend="numpy")


def test_invalid_dtype_backend():
    msg = (
        "dtype_backend numpy is invalid, only 'numpy_nullable' and "
        "'pyarrow' are allowed."
    )
    with pytest.raises(ValueError, match=msg):
        pd.read_spss("test", dtype_backend="numpy")


def test_invalid_dtype_backend():
    ser = Series([1, 2, 3])
    msg = (
        "dtype_backend numpy is invalid, only 'numpy_nullable' and "
        "'pyarrow' are allowed."
    )
    with pytest.raises(ValueError, match=msg):
        to_numeric(ser, dtype_backend="numpy")


def test_invalid_dtype_backend():
    msg = (
        "dtype_backend numpy is invalid, only 'numpy_nullable' and "
        "'pyarrow' are allowed."
    )
    with pytest.raises(ValueError, match=msg):
        read_fwf("test", dtype_backend="numpy")


def test_invalid_dtype_backend(all_parsers):
    parser = all_parsers
    msg = (
        "dtype_backend numpy is invalid, only 'numpy_nullable' and "
        "'pyarrow' are allowed."
    )
    with pytest.raises(ValueError, match=msg):
        parser.read_csv("test", dtype_backend="numpy")


def test_invalid_dtype_backend():
    msg = (
        "dtype_backend numpy is invalid, only 'numpy_nullable' and "
        "'pyarrow' are allowed."
    )
    with pytest.raises(ValueError, match=msg):
        read_xml("test", dtype_backend="numpy")

