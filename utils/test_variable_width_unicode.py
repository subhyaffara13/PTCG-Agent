
def test_variable_width_unicode():
    data = """
שלום שלום
ום   שלל
של   ום
""".strip("\r\n")
    encoding = "utf8"
    kwargs = {"header": None, "encoding": encoding}

    expected = read_fwf(
        BytesIO(data.encode(encoding)), colspecs=[(0, 4), (5, 9)], **kwargs
    )
    result = read_fwf(BytesIO(data.encode(encoding)), **kwargs)
    tm.assert_frame_equal(result, expected)

