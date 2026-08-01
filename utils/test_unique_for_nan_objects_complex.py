
def test_unique_for_nan_objects_complex():
    table = ht.PyObjectHashTable()
    keys = np.array([complex(float("nan"), 1.0) for i in range(50)], dtype=np.object_)
    unique = table.unique(keys)
    assert len(unique) == 1

