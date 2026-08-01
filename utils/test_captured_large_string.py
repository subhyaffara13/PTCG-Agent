
def test_captured_large_string(capsys):
    # Make this bigger than the buffer used on the C++ side: 1024 chars
    msg = "I've been redirected to Python, I hope!"
    msg = msg * (1024 // len(msg) + 1)

    m.captured_output_default(msg)
    stdout, stderr = capsys.readouterr()
    assert stdout == msg
    assert not stderr

