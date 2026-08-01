
def test_path_deepcopy():
    # Should not raise any error
    verts = [[0, 0], [1, 1]]
    codes = [Path.MOVETO, Path.LINETO]
    path1 = Path(verts, readonly=True)
    path2 = Path(verts, codes, readonly=True)
    path1_copy = path1.deepcopy()
    path2_copy = path2.deepcopy()
    assert path1 is not path1_copy
    assert path1.vertices is not path1_copy.vertices
    assert_array_equal(path1.vertices, path1_copy.vertices)
    assert path1.readonly
    assert not path1_copy.readonly
    assert path2 is not path2_copy
    assert path2.vertices is not path2_copy.vertices
    assert_array_equal(path2.vertices, path2_copy.vertices)
    assert path2.codes is not path2_copy.codes
    assert_array_equal(path2.codes, path2_copy.codes)
    assert path2.readonly
    assert not path2_copy.readonly

