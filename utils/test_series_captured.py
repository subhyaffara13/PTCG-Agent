
def test_series_captured(capture):
    with capture:
        m.captured_output("a")
        m.captured_output("b")
    assert capture == "ab"

