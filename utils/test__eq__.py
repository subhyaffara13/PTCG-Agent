
def test__eq__():
    class My(object):
        def __iter__(self):
            yield 1
            yield 2
            return
        def __getitem__(self, i):
            return list(self)[i]
    a = Matrix(2, 1, [1, 2])
    assert a != My()
    class My_sympy(My):
        def _sympy_(self):
            return Matrix(self)
    assert a == My_sympy()


def test__eq__():
    class My(object):
        def __iter__(self):
            yield 1
            yield 2
            return
        def __getitem__(self, i):
            return list(self)[i]
    a = Matrix(2, 1, [1, 2])
    assert a != My()
    class My_sympy(My):
        def _sympy_(self):
            return Matrix(self)
    assert a == My_sympy()

