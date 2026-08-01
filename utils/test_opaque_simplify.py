
def test_opaque_simplify():
    """Test that we can read a MatlabOpaque object when simplify_cells=True."""
    data = loadmat(pjoin(test_data_path, 'parabola.mat'), simplify_cells=True)
    assert isinstance(data['parabola'], MatlabFunction)

