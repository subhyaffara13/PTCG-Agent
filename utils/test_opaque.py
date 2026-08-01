
def test_opaque():
    """Test that we can read a MatlabOpaque object."""
    data = loadmat(pjoin(test_data_path, 'parabola.mat'))
    assert isinstance(data['parabola'], MatlabFunction)
    assert isinstance(data['parabola'].item()[3].item()[3], MatlabOpaque)

