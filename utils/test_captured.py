
def test_captured(capsys):
    msg = "I've been redirected to Python, I hope!"
    m.captured_output(msg)
    stdout, stderr = capsys.readouterr()
    assert stdout == msg
    assert not stderr

    m.captured_output_default(msg)
    stdout, stderr = capsys.readouterr()
    assert stdout == msg
    assert not stderr

    m.captured_err(msg)
    stdout, stderr = capsys.readouterr()
    assert not stdout
    assert stderr == msg

