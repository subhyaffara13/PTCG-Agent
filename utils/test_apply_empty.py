
def test_apply_empty(func, engine):
    # empty
    empty_frame = DataFrame()

    result = empty_frame.apply(func, engine=engine)
    assert result.empty

