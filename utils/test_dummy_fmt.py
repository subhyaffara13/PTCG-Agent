
def test_dummy_fmt():
    with warns_deprecated_sympy():
        TensorIndexType('Lorentz', dummy_fmt='L')

