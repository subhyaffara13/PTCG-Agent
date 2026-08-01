
def test_TensorType():
    with warns_deprecated_sympy():
        sym2 = TensorSymmetry.fully_symmetric(2)
        Lorentz = TensorIndexType('Lorentz')
        S2 = TensorType([Lorentz]*2, sym2)
        assert isinstance(S2, TensorType)

