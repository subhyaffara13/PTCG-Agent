
def test_chunksize_with_usecols_second_block_shorter(all_parsers):
    # GH#21211
    parser = all_parsers
    data = """1,2,3,4
5,6,7,8
9,10,11
"""

    if parser.engine == "pyarrow":
        msg = "The 'chunksize' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(
                StringIO(data),
                names=["a", "b"],
                chunksize=2,
                usecols=[0, 1],
                header=None,
            )
        return

    result_chunks = parser.read_csv(
        StringIO(data),
        names=["a", "b"],
        chunksize=2,
        usecols=[0, 1],
        header=None,
    )

    expected_frames = [
        DataFrame({"a": [1, 5], "b": [2, 6]}),
        DataFrame({"a": [9], "b": [10]}, index=[2]),
    ]

    for i, result in enumerate(result_chunks):
        tm.assert_frame_equal(result, expected_frames[i])

