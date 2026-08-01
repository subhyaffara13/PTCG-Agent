
def test_temporary_file(all_parsers, temp_file):
    # see gh-13398
    parser = all_parsers
    data = "0 0"

    with temp_file.open(mode="w+", encoding="utf-8") as new_file:
        new_file.write(data)
        new_file.flush()
        new_file.seek(0)

        if parser.engine == "pyarrow":
            msg = "the 'pyarrow' engine does not support regex separators"
            with pytest.raises(ValueError, match=msg):
                parser.read_csv(new_file, sep=r"\s+", header=None)
            return

        result = parser.read_csv(new_file, sep=r"\s+", header=None)

        expected = DataFrame([[0, 0]])
        tm.assert_frame_equal(result, expected)

