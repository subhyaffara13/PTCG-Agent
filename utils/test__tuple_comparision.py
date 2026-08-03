from typing import Tuple

def test_Tuple_comparision():
    assert (Tuple(1, 3) >= Tuple(-10, 30)) is S.true
    assert (Tuple(1, 3) <= Tuple(-10, 30)) is S.false
    assert (Tuple(1, 3) >= Tuple(1, 3)) is S.true
    assert (Tuple(1, 3) <= Tuple(1, 3)) is S.true

