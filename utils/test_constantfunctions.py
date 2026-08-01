
def test_constantfunctions():
    with warns_deprecated_sympy():
        tf = aesara_function([],[1+1j])
    assert(tf()==1+1j)


def test_constantfunctions():
    with warns_deprecated_sympy():
        tf = theano_function_([],[1+1j])
    assert(tf()==1+1j)

