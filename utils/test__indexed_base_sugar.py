from typing import Tuple

def test_IndexedBase_sugar():
    i, j = symbols('i j', integer=True)
    a = symbols('a')
    A1 = Indexed(a, i, j)
    A2 = IndexedBase(a)
    assert A1 == A2[i, j]
    assert A1 == A2[(i, j)]
    assert A1 == A2[[i, j]]
    assert A1 == A2[Tuple(i, j)]
    assert all(a.is_Integer for a in A2[1, 0].args[1:])

