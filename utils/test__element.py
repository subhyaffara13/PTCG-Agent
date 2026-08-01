
def test_Element():
    assert ccode(Element('x', 'ij')) == 'x[i][j]'
    assert ccode(Element('x', 'ij', strides='kl', offset='o')) == 'x[i*k + j*l + o]'
    assert ccode(Element('x', (3,))) == 'x[3]'
    assert ccode(Element('x', (3,4,5))) == 'x[3][4][5]'

