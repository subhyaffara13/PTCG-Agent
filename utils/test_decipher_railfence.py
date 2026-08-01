
def test_decipher_railfence():
    assert decipher_railfence("hlowrdel ol",2) == "hello world"
    assert decipher_railfence("horel ollwd",3) == "hello world"
    assert decipher_railfence("hwe olordll",4) == "hello world"

