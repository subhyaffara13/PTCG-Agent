
def test_TensExpr():
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    a, b, c, d = tensor_indices('a,b,c,d', Lorentz)
    g = Lorentz.metric
    A, B = tensor_heads('A B', [Lorentz]*2, TensorSymmetry.fully_symmetric(2))
    raises(ValueError, lambda: g(c, d)/g(a, b))
    raises(ValueError, lambda: S.One/g(a, b))
    raises(ValueError, lambda: (A(c, d) + g(c, d))/g(a, b))
    raises(ValueError, lambda: S.One/(A(c, d) + g(c, d)))
    raises(ValueError, lambda: A(a, b) + A(a, c))

    #t = A(a, b) + B(a, b) # assigned to t for below
    #raises(NotImplementedError, lambda: TensExpr.__mul__(t, 'a'))
    #raises(NotImplementedError, lambda: TensExpr.__add__(t, 'a'))
    #raises(NotImplementedError, lambda: TensExpr.__radd__(t, 'a'))
    #raises(NotImplementedError, lambda: TensExpr.__sub__(t, 'a'))
    #raises(NotImplementedError, lambda: TensExpr.__rsub__(t, 'a'))
    #raises(NotImplementedError, lambda: TensExpr.__truediv__(t, 'a'))
    #raises(NotImplementedError, lambda: TensExpr.__rtruediv__(t, 'a'))
    with warns_deprecated_sympy():
        # DO NOT REMOVE THIS AFTER DEPRECATION REMOVED:
        raises(ValueError, lambda: A(a, b)**2)
    raises(NotImplementedError, lambda: 2**A(a, b))
    raises(NotImplementedError, lambda: abs(A(a, b)))

