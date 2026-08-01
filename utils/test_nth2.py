
def test_nth2():
    # out of bounds, regression from 0.13.1
    # GH 6621
    df = DataFrame(
        {
            "color": {0: "green", 1: "green", 2: "red", 3: "red", 4: "red"},
            "food": {0: "ham", 1: "eggs", 2: "eggs", 3: "ham", 4: "pork"},
            "two": {
                0: 1.5456590000000001,
                1: -0.070345000000000005,
                2: -2.4004539999999999,
                3: 0.46206000000000003,
                4: 0.52350799999999997,
            },
            "one": {
                0: 0.56573799999999996,
                1: -0.9742360000000001,
                2: 1.033801,
                3: -0.78543499999999999,
                4: 0.70422799999999997,
            },
        }
    ).set_index(["color", "food"])

    result = df.groupby(level=0, as_index=False).nth(2)
    expected = df.iloc[[-1]]
    tm.assert_frame_equal(result, expected)

    result = df.groupby(level=0, as_index=False).nth(3)
    expected = df.loc[[]]
    tm.assert_frame_equal(result, expected)

