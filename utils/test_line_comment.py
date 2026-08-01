
def test_line_comment(all_parsers, read_kwargs):
    parser = all_parsers
    data = """# empty
A,B,C
1,2.,4.#hello world
#ignore this line
5.,NaN,10.0
"""
    if read_kwargs.get("sep"):
        data = data.replace(",", " ")
    elif read_kwargs.get("lineterminator"):
        data = data.replace("\n", read_kwargs.get("lineterminator"))

    read_kwargs["comment"] = "#"
    if parser.engine == "pyarrow":
        if "lineterminator" in read_kwargs:
            msg = (
                "The 'lineterminator' option is not supported with the 'pyarrow' engine"
            )
        else:
            msg = "The 'comment' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO(data), **read_kwargs)
        return
    elif parser.engine == "python" and read_kwargs.get("lineterminator"):
        msg = r"Custom line terminators not supported in python parser \(yet\)"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO(data), **read_kwargs)
        return

    result = parser.read_csv(StringIO(data), **read_kwargs)
    expected = DataFrame(
        [[1.0, 2.0, 4.0], [5.0, np.nan, 10.0]], columns=["A", "B", "C"]
    )
    tm.assert_frame_equal(result, expected)

