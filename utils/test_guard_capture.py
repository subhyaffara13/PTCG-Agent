
def test_guard_capture(capsys):
    msg = "I've been redirected to Python, I hope!"
    m.guard_output(msg)
    stdout, stderr = capsys.readouterr()
    assert stdout == msg
    assert not stderr

