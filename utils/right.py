
def right():
    return DataFrame(
        {
            "X": Series(["foo", "bar"]).astype(CategoricalDtype(["foo", "bar"])),
            "Z": [1, 2],
        }
    )


def right():
    return DataFrame({"key": ["b", "c", "d", "f"], "rvalue": [1, 2, 3.0, 4]})


def right(multiindex_dataframe_random_data):
    """right dataframe (multi-indexed) for multi-index join tests"""
    df = multiindex_dataframe_random_data
    df.index.names = ["key1", "key2"]

    df.columns = ["j_one", "j_two", "j_three"]
    return df

