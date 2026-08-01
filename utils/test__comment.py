
def test_Comment():
    c = Comment('foobar')
    assert c.text == 'foobar'
    assert str(c) == 'foobar'

