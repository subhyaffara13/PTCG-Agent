
def test_encode_pth():
    """Ensure _encode_pth function does not produce encoding warnings"""
    content = _encode_pth("tkmilan_ç_utf8")  # no warnings (would be turned into errors)
    assert isinstance(content, bytes)

