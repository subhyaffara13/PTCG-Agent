
def test_encipher_railfence():
    assert encipher_railfence("hello world",2) == "hlowrdel ol"
    assert encipher_railfence("hello world",3) == "horel ollwd"
    assert encipher_railfence("hello world",4) == "hwe olordll"

