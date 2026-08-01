
def test_array_equivalent_index_with_tuples():
    # GH#48446
    idx1 = Index(np.array([(pd.NA, 4), (1, 1)], dtype="object"))
    idx2 = Index(np.array([(1, 1), (pd.NA, 4)], dtype="object"))
    assert not array_equivalent(idx1, idx2)
    assert not idx1.equals(idx2)
    assert not array_equivalent(idx2, idx1)
    assert not idx2.equals(idx1)

    idx1 = Index(np.array([(4, pd.NA), (1, 1)], dtype="object"))
    idx2 = Index(np.array([(1, 1), (4, pd.NA)], dtype="object"))
    assert not array_equivalent(idx1, idx2)
    assert not idx1.equals(idx2)
    assert not array_equivalent(idx2, idx1)
    assert not idx2.equals(idx1)

