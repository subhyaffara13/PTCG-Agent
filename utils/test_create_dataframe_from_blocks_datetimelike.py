
def test_create_dataframe_from_blocks_datetimelike():
    # extension dtypes that have an exact matching numpy dtype can also be
    # be passed as a numpy array
    index, columns = pd.RangeIndex(3), pd.Index(["a", "b", "c", "d"])

    block_array1 = np.arange(
        datetime.datetime(2020, 1, 1),
        datetime.datetime(2020, 1, 7),
        step=datetime.timedelta(1),
    ).reshape((2, 3))
    block_array2 = np.arange(
        datetime.timedelta(1), datetime.timedelta(7), step=datetime.timedelta(1)
    ).reshape((2, 3))
    result = create_dataframe_from_blocks(
        [(block_array1, np.array([0, 2])), (block_array2, np.array([1, 3]))],
        index=index,
        columns=columns,
    )
    expected = pd.DataFrame(
        {
            "a": pd.date_range("2020-01-01", periods=3, unit="us"),
            "b": pd.timedelta_range("1 days", periods=3, unit="us"),
            "c": pd.date_range("2020-01-04", periods=3, unit="us"),
            "d": pd.timedelta_range("4 days", periods=3, unit="us"),
        }
    )
    tm.assert_frame_equal(result, expected)

