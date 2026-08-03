from typing import Tuple

def test__aresame():
    assert not _aresame(Basic(Tuple()), Basic())
    for i, j in [(S(2), S(2.)), (1., Float(1))]:
        for do in range(2):
            assert not _aresame(Basic(i), Basic(j))
            assert not _aresame(i, j)
            i, j = j, i

