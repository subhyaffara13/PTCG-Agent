
def test_readcsv_memmap_utf8(all_parsers, temp_file):
    """
    GH 43787

    Test correct handling of UTF-8 chars when memory_map=True and encoding is UTF-8
    """
    lines = []
    line_length = 128
    start_char = " "
    end_char = "\U00010080"
    # This for loop creates a list of 128-char strings
    # consisting of consecutive Unicode chars
    for lnum in range(ord(start_char), ord(end_char), line_length):
        line = "".join([chr(c) for c in range(lnum, lnum + 0x80)]) + "\n"
        try:
            line.encode("utf-8")
        except UnicodeEncodeError:
            continue
        lines.append(line)
    parser = all_parsers
    df = DataFrame(lines)
    df.to_csv(temp_file, index=False, header=False, encoding="utf-8")

    if parser.engine == "pyarrow":
        msg = "The 'memory_map' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(temp_file, header=None, memory_map=True, encoding="utf-8")
        return

    dfr = parser.read_csv(temp_file, header=None, memory_map=True, encoding="utf-8")
    tm.assert_frame_equal(df, dfr)

