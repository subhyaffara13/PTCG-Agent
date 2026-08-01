
def test_triangulation_init():
    x = [-1, 0, 1, 0]
    y = [0, -1, 0, 1]
    with pytest.raises(ValueError, match="x and y must be equal-length"):
        mtri.Triangulation(x, [1, 2])
    with pytest.raises(
            ValueError,
            match=r"triangles must be a \(N, 3\) int array, but found shape "
                  r"\(3,\)"):
        mtri.Triangulation(x, y, [0, 1, 2])
    with pytest.raises(
            ValueError,
            match=r"triangles must be a \(N, 3\) int array, not 'other'"):
        mtri.Triangulation(x, y, 'other')
    with pytest.raises(ValueError, match="found value 99"):
        mtri.Triangulation(x, y, [[0, 1, 99]])
    with pytest.raises(ValueError, match="found value -1"):
        mtri.Triangulation(x, y, [[0, 1, -1]])

