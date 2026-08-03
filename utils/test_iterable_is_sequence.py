from typing import Tuple

def test_iterable_is_sequence():
    ordered = [[], (), Tuple(), Matrix([[]])]
    unordered = [set()]
    not_sympy_iterable = [{}, '', '']
    assert all(is_sequence(i) for i in ordered)
    assert all(not is_sequence(i) for i in unordered)
    assert all(iterable(i) for i in ordered + unordered)
    assert all(not iterable(i) for i in not_sympy_iterable)
    assert all(iterable(i, exclude=None) for i in not_sympy_iterable)

