
def test_is_palindromic():
    assert is_palindromic('')
    assert is_palindromic('x')
    assert is_palindromic('xx')
    assert is_palindromic('xyx')
    assert not is_palindromic('xy')
    assert not is_palindromic('xyzx')
    assert is_palindromic('xxyzzyx', 1)
    assert not is_palindromic('xxyzzyx', 2)
    assert is_palindromic('xxyzzyx', 2, -1)
    assert is_palindromic('xxyzzyx', 2, 6)
    assert is_palindromic('xxyzyx', 1)
    assert not is_palindromic('xxyzyx', 2)
    assert is_palindromic('xxyzyx', 2, 2 + 3)


def test_is_palindromic():
    assert is_palindromic(-11)
    assert is_palindromic(11)
    assert is_palindromic(0o121, 8)
    assert not is_palindromic(123)

