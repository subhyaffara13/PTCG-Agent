
def test_bad_stream_exception(all_parsers, csv_dir_path):
    # see gh-13652
    #
    # This test validates that both the Python engine and C engine will
    # raise UnicodeDecodeError instead of C engine raising ParserError
    # and swallowing the exception that caused read to fail.
    path = os.path.join(csv_dir_path, "sauron.SHIFT_JIS.csv")
    codec = codecs.lookup("utf-8")
    utf8 = codecs.lookup("utf-8")
    parser = all_parsers
    msg = "'utf-8' codec can't decode byte"

    # Stream must be binary UTF8.
    with (
        open(path, "rb") as handle,
        codecs.StreamRecoder(
            handle, utf8.encode, utf8.decode, codec.streamreader, codec.streamwriter
        ) as stream,
    ):
        with pytest.raises(UnicodeDecodeError, match=msg):
            parser.read_csv(stream)

