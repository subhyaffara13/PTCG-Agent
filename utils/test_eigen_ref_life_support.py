
def test_eigen_ref_life_support():
    """Ensure the lifetime of temporary arrays created by the `Ref` caster

    The `Ref` caster sometimes creates a copy which needs to stay alive. This needs to
    happen both for directs casts (just the array) or indirectly (e.g. list of arrays).
    """

    a = np.full(shape=10, fill_value=8, dtype=np.int8)
    assert m.get_elem_direct(a) == 8

    list_of_a = [a]
    assert m.get_elem_indirect(list_of_a) == 8

