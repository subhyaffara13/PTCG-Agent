
def test_step(step):
    # Test slice with various step values
    data = [["x", f"x{i}"] for i in range(5)]
    data += [["y", f"y{i}"] for i in range(4)]
    data += [["z", f"z{i}"] for i in range(3)]
    df = pd.DataFrame(data, columns=["A", "B"])

    grouped = df.groupby("A", as_index=False)

    result = grouped._positional_selector[::step]

    data = [["x", f"x{i}"] for i in range(0, 5, step)]
    data += [["y", f"y{i}"] for i in range(0, 4, step)]
    data += [["z", f"z{i}"] for i in range(0, 3, step)]

    index = [0 + i for i in range(0, 5, step)]
    index += [5 + i for i in range(0, 4, step)]
    index += [9 + i for i in range(0, 3, step)]

    expected = pd.DataFrame(data, columns=["A", "B"], index=index)

    tm.assert_frame_equal(result, expected)

