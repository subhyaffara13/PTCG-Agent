import uuid

def test_internal_eof_byte_to_file(all_parsers, temp_file):
    # see gh-16559
    parser = all_parsers
    data = b'c1,c2\r\n"test \x1a    test", test\r\n'
    expected = DataFrame([["test \x1a    test", " test"]], columns=["c1", "c2"])
    path = f"__{uuid.uuid4()}__.csv"

    path2 = temp_file.parent / path
    with open(path2, "wb") as f:
        f.write(data)

    result = parser.read_csv(path2)
    tm.assert_frame_equal(result, expected)

