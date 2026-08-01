
def test_bool_header_arg(all_parsers, header):
    # see gh-6114
    parser = all_parsers
    data = """\
MyColumn
a
b
a
b"""
    msg = "Passing a bool to header is invalid"
    with pytest.raises(TypeError, match=msg):
        parser.read_csv(StringIO(data), header=header)


def test_bool_header_arg(header):
    # see gh-6114
    data = """\
MyColumn
   a
   b
   a
   b"""

    msg = "Passing a bool to header is invalid"
    with pytest.raises(TypeError, match=msg):
        read_fwf(StringIO(data), header=header)

