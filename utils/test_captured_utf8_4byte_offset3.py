
def test_captured_utf8_4byte_offset3(capsys):
    msg = "\U0010FFFF"
    msg = "123" + msg * (1024 // len(msg) + 1)

    m.captured_output_default(msg)
    stdout, stderr = capsys.readouterr()
    assert stdout == msg
    assert not stderr

