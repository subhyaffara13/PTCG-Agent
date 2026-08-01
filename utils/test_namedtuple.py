
def test_namedtuple():
    assert Z is dill.loads(dill.dumps(Z))
    assert Zi == dill.loads(dill.dumps(Zi))
    assert X is dill.loads(dill.dumps(X))
    assert Xi == dill.loads(dill.dumps(Xi))
    assert Defaults is dill.loads(dill.dumps(Defaults))
    assert Defaultsi == dill.loads(dill.dumps(Defaultsi))
    assert Bad is not dill.loads(dill.dumps(Bad))
    assert Bad._fields == dill.loads(dill.dumps(Bad))._fields
    assert tuple(Badi) == tuple(dill.loads(dill.dumps(Badi)))

    class A:
        class B(namedtuple("C", ["one", "two"])):
            '''docstring'''
        B.__module__ = 'testing'

    a = A()
    assert dill.copy(a)

    assert dill.copy(A.B).__name__ == 'B'
    assert dill.copy(A.B).__qualname__.endswith('.<locals>.A.B')
    assert dill.copy(A.B).__doc__ == 'docstring'
    assert dill.copy(A.B).__module__ == 'testing'

    from typing import NamedTuple

    def A():
        class B(NamedTuple):
            x: int
        return B

    assert type(dill.copy(A()(8))).__qualname__ == type(A()(8)).__qualname__

