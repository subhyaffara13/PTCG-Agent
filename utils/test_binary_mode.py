
def test_binary_mode(temp_file):
    """
    read_fwf supports opening files in binary mode.

    GH 18035.
    """
    data = """aaa aaa aaa
bba bab b a"""
    df_reference = DataFrame(
        [["bba", "bab", "b a"]], columns=["aaa", "aaa.1", "aaa.2"], index=[0]
    )
    path = temp_file
    path.write_text(data, encoding="utf-8")
    with open(path, "rb") as file:
        df = read_fwf(file)
        file.seek(0)
        tm.assert_frame_equal(df, df_reference)

