
def test_multi_captured(capfd):
    stream = StringIO()
    with redirect_stdout(stream):
        m.captured_output("a")
        m.raw_output("b")
        m.captured_output("c")
        m.raw_output("d")
    stdout, stderr = capfd.readouterr()
    assert stdout == "bd"
    assert stream.getvalue() == "ac"

