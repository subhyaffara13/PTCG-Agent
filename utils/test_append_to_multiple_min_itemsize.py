
def test_append_to_multiple_min_itemsize(temp_hdfstore):
    # GH 11238
    df = DataFrame(
        {
            "IX": np.arange(1, 21),
            "Num": np.arange(1, 21),
            "BigNum": np.arange(1, 21) * 88,
            "Str": ["a" for _ in range(20)],
            "LongStr": ["abcde" for _ in range(20)],
        }
    )
    expected = df.iloc[[0]]
    # Reading/writing RangeIndex info is not supported yet
    expected.index = Index(list(range(len(expected.index))))

    temp_hdfstore.append_to_multiple(
        {
            "index": ["IX"],
            "nums": ["Num", "BigNum"],
            "strs": ["Str", "LongStr"],
        },
        df.iloc[[0]],
        "index",
        min_itemsize={"Str": 10, "LongStr": 100, "Num": 2},
    )
    result = temp_hdfstore.select_as_multiple(["index", "nums", "strs"])
    tm.assert_frame_equal(result, expected, check_index_type=True)

