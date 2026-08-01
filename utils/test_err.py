
def test_err(capfd):
    msg = "Something that should not show up in log"
    stream = StringIO()
    with redirect_stderr(stream):
        m.raw_err(msg)
    stdout, stderr = capfd.readouterr()
    assert not stdout
    assert stderr == msg
    assert not stream.getvalue()

    stream = StringIO()
    with redirect_stderr(stream):
        m.captured_err(msg)
    stdout, stderr = capfd.readouterr()
    assert not stdout
    assert not stderr
    assert stream.getvalue() == msg

