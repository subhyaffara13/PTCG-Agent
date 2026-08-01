
def test_is_hermitian():
    a = PropertiesOnlyMatrix([[1, I], [-I, 1]])
    assert a.is_hermitian
    a = PropertiesOnlyMatrix([[2*I, I], [-I, 1]])
    assert a.is_hermitian is False
    a = PropertiesOnlyMatrix([[x, I], [-I, 1]])
    assert a.is_hermitian is None
    a = PropertiesOnlyMatrix([[x, 1], [-I, 1]])
    assert a.is_hermitian is False


def test_is_hermitian():
    a = Matrix([[1, I], [-I, 1]])
    assert a.is_hermitian
    a = Matrix([[2*I, I], [-I, 1]])
    assert a.is_hermitian is False
    a = Matrix([[x, I], [-I, 1]])
    assert a.is_hermitian is None
    a = Matrix([[x, 1], [-I, 1]])
    assert a.is_hermitian is False

