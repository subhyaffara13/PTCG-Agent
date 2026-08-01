
def test_collection_set_verts_array():
    verts = np.arange(80, dtype=np.double).reshape(10, 4, 2)
    col_arr = PolyCollection(verts)
    col_list = PolyCollection(list(verts))
    assert len(col_arr._paths) == len(col_list._paths)
    for ap, lp in zip(col_arr._paths, col_list._paths):
        assert np.array_equal(ap._vertices, lp._vertices)
        assert np.array_equal(ap._codes, lp._codes)

    verts_tuple = np.empty(10, dtype=object)
    verts_tuple[:] = [tuple(tuple(y) for y in x) for x in verts]
    col_arr_tuple = PolyCollection(verts_tuple)
    assert len(col_arr._paths) == len(col_arr_tuple._paths)
    for ap, atp in zip(col_arr._paths, col_arr_tuple._paths):
        assert np.array_equal(ap._vertices, atp._vertices)
        assert np.array_equal(ap._codes, atp._codes)

