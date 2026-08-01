
def test_ewma_frame(frame, name):
    frame_result = getattr(frame.ewm(com=10), name)()
    assert isinstance(frame_result, DataFrame)

