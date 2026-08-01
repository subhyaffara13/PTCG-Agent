
def test_bytes_io_input(all_parsers):
    encoding = "cp1255"
    parser = all_parsers

    data = BytesIO("שלום:1234\n562:123".encode(encoding))
    result = parser.read_csv(data, sep=":", encoding=encoding)

    expected = DataFrame([[562, 123]], columns=["שלום", "1234"])
    tm.assert_frame_equal(result, expected)


def test_bytes_io_input():
    data = BytesIO("שלום\nשלום".encode())  # noqa: RUF001
    result = read_fwf(data, widths=[2, 2], encoding="utf8")
    expected = DataFrame([["של", "ום"]], columns=["של", "ום"])
    tm.assert_frame_equal(result, expected)

