
def test_open_file(all_parsers, temp_file):
    # GH 39024
    parser = all_parsers

    msg = "Could not determine delimiter"
    err = csv.Error
    if parser.engine == "c":
        msg = "object of type 'NoneType' has no len"
        err = TypeError
    elif parser.engine == "pyarrow":
        msg = "'utf-8' codec can't decode byte 0xe4"
        err = ValueError

    file = Path(temp_file)
    file.write_bytes(b"\xe4\na\n1")

    with tm.assert_produces_warning(None):
        # should not trigger a ResourceWarning
        with pytest.raises(err, match=msg):
            parser.read_csv(file, sep=None, encoding_errors="replace")

