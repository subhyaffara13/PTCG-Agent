
def test_transform_coercion():
    # 14457
    # when we are transforming be sure to not coerce
    # via assignment
    df = DataFrame({"A": ["a", "a", "b", "b"], "B": [0, 1, 3, 4]})
    g = df.groupby("A")

    expected = g.transform(np.mean)
    result = g.transform(lambda x: np.mean(x, axis=0))
    tm.assert_frame_equal(result, expected)

