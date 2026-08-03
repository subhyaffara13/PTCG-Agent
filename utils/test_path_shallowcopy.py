from pathlib import Path


def test_path_shallowcopy():
    # Should not raise any error
    verts = [[0, 0], [1, 1]]
    codes = [Path.MOVETO, Path.LINETO]
    path1 = Path(verts)
    path2 = Path(verts, codes)
    path1_copy = path1.copy()
    path2_copy = path2.copy()
    assert path1 is not path1_copy
    assert path1.vertices is path1_copy.vertices
    assert path2 is not path2_copy
    assert path2.vertices is path2_copy.vertices
    assert path2.codes is path2_copy.codes

