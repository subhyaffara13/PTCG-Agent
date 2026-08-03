import time

def test_transform_casting():
    # 13046
    times = [
        "13:43:27",
        "14:26:19",
        "14:29:01",
        "18:39:34",
        "18:40:18",
        "18:44:30",
        "18:46:00",
        "18:52:15",
        "18:59:59",
        "19:17:48",
        "19:21:38",
    ]
    df = DataFrame(
        {
            "A": [f"B-{i}" for i in range(11)],
            "ID3": np.take(
                ["a", "b", "c", "d", "e"], [0, 1, 2, 1, 3, 1, 1, 1, 4, 1, 1]
            ),
            "DATETIME": pd.to_datetime([f"2014-10-08 {time}" for time in times]),
        },
        index=pd.RangeIndex(11, name="idx"),
    )

    result = df.groupby("ID3")["DATETIME"].transform(lambda x: x.diff())
    assert lib.is_np_dtype(result.dtype, "m")

    result = df[["ID3", "DATETIME"]].groupby("ID3").transform(lambda x: x.diff())
    assert lib.is_np_dtype(result.DATETIME.dtype, "m")

