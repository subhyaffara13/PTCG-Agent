
def test_encoding_memory_map(all_parsers, encoding, temp_file):
    # GH40986
    parser = all_parsers
    expected = DataFrame(
        {
            "name": ["Raphael", "Donatello", "Miguel Angel", "Leonardo"],
            "mask": ["red", "purple", "orange", "blue"],
            "weapon": ["sai", "bo staff", "nunchunk", "katana"],
        }
    )
    expected.to_csv(temp_file, index=False, encoding=encoding)

    if parser.engine == "pyarrow":
        msg = "The 'memory_map' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(temp_file, encoding=encoding, memory_map=True)
        return

    df = parser.read_csv(temp_file, encoding=encoding, memory_map=True)
    tm.assert_frame_equal(df, expected)

