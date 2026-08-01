
def test_no_permission(all_parsers, temp_file):
    # GH 23784
    parser = all_parsers

    msg = r"\[Errno 13\]"
    path = temp_file
    os.chmod(path, 0)  # make file unreadable

    # verify that this process cannot open the file (not running as sudo)
    try:
        with open(path, encoding="utf-8"):
            pass
        pytest.skip("Running as sudo.")
    except PermissionError:
        pass

    with pytest.raises(PermissionError, match=msg) as e:
        parser.read_csv(path)
    assert str(path.resolve()) == e.value.filename

