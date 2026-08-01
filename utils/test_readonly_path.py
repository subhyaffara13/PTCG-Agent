
def test_readonly_path():
    path = Path.unit_circle()

    def modify_vertices():
        path.vertices = path.vertices * 2.0

    with pytest.raises(AttributeError):
        modify_vertices()

