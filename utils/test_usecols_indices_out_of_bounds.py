
def test_usecols_indices_out_of_bounds(all_parsers, names):
    # GH#25623 & GH 41130; enforced in 2.0
    parser = all_parsers
    data = """
a,b
1,2
    """

    err = ParserError
    msg = "Defining usecols with out-of-bounds"
    if parser.engine == "pyarrow":
        err = ValueError
        msg = _msg_pyarrow_requires_names

    with pytest.raises(err, match=msg):
        parser.read_csv(StringIO(data), usecols=[0, 2], names=names, header=0)

