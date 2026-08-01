
def test_generic():
    # https://github.com/sympy/sympy/issues/25399
    class A(Symbol, Generic[T]):
        pass

    class B(A[T]):
        pass

