
def test_redirect_err(capfd):
    msg = "StdOut"
    msg2 = "StdErr"

    stream = StringIO()
    with redirect_stderr(stream), m.ostream_redirect(stdout=False):
        m.raw_output(msg)
        m.raw_err(msg2)
    stdout, stderr = capfd.readouterr()
    assert stdout == msg
    assert not stderr
    assert stream.getvalue() == msg2

