
def test_sizeof():
    typename = 'unsigned int'
    sz = sizeof(typename)
    assert ccode(sz) == 'sizeof(%s)' % typename
    assert sz.func(*sz.args) == sz
    assert not sz.is_Atom
    assert sz.atoms() == {String('unsigned int'), String('sizeof')}

