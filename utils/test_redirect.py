
def test_redirect(capfd):
    msg = "Should not be in log!"
    stream = StringIO()
    with redirect_stdout(stream):
        m.raw_output(msg)
    stdout, stderr = capfd.readouterr()
    assert stdout == msg
    assert not stream.getvalue()

    stream = StringIO()
    with redirect_stdout(stream), m.ostream_redirect():
        m.raw_output(msg)
    stdout, stderr = capfd.readouterr()
    assert not stdout
    assert stream.getvalue() == msg

    stream = StringIO()
    with redirect_stdout(stream):
        m.raw_output(msg)
    stdout, stderr = capfd.readouterr()
    assert stdout == msg
    assert not stream.getvalue()

