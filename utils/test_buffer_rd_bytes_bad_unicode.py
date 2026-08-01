
def test_buffer_rd_bytes_bad_unicode(c_parser_only):
    # see gh-22748
    t = BytesIO(b"\xb0")
    t = TextIOWrapper(t, encoding="UTF-8", errors="surrogateescape")
    msg = "'utf-8' codec can't encode character"
    with pytest.raises(UnicodeError, match=msg):
        c_parser_only.read_csv(t, encoding="UTF-8")

