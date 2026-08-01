
def test_apply_empty_except_index(engine):
    # GH 2476
    expected = DataFrame(index=["a"])
    result = expected.apply(lambda x: x["a"], axis=1, engine=engine)
    tm.assert_frame_equal(result, expected)

