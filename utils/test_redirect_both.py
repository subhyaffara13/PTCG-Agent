
def test_redirect_both(capfd):
    msg = "StdOut"
    msg2 = "StdErr"

    stream = StringIO()
    stream2 = StringIO()
    with redirect_stdout(stream), redirect_stderr(stream2), m.ostream_redirect():
        m.raw_output(msg)
        m.raw_err(msg2)
    stdout, stderr = capfd.readouterr()
    assert not stdout
    assert not stderr
    assert stream.getvalue() == msg
    assert stream2.getvalue() == msg2

