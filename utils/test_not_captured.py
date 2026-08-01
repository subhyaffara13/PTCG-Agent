
def test_not_captured(capfd):
    msg = "Something that should not show up in log"
    stream = StringIO()
    with redirect_stdout(stream):
        m.raw_output(msg)
    stdout, stderr = capfd.readouterr()
    assert stdout == msg
    assert not stderr
    assert not stream.getvalue()

    stream = StringIO()
    with redirect_stdout(stream):
        m.captured_output(msg)
    stdout, stderr = capfd.readouterr()
    assert not stdout
    assert not stderr
    assert stream.getvalue() == msg

