
def test_captured_utf8_3byte_offset2(capsys):
    msg = "\uFFFF"
    msg = "12" + msg * (1024 // len(msg) + 1)

    m.captured_output_default(msg)
    stdout, stderr = capsys.readouterr()
    assert stdout == msg
    assert not stderr

