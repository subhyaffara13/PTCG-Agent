
def test_chunk_splits_multibyte_char(all_parsers, temp_file):
    """
    Chunk splits a multibyte character with memory_map=True

    GH 43540
    """
    parser = all_parsers
    # DEFAULT_CHUNKSIZE = 262144, defined in parsers.pyx
    df = DataFrame(data=["a" * 127] * 2048)

    # Put two-bytes utf-8 encoded character "ą" at the end of chunk
    # utf-8 encoding of "ą" is b'\xc4\x85'
    df.iloc[2047] = "a" * 127 + "ą"
    df.to_csv(temp_file, index=False, header=False, encoding="utf-8")

    if parser.engine == "pyarrow":
        msg = "The 'memory_map' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(temp_file, header=None, memory_map=True)
        return

    dfr = parser.read_csv(temp_file, header=None, memory_map=True)
    tm.assert_frame_equal(dfr, df)

