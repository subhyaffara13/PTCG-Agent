
def test_matlab_string_opaque():
    """Test that we can read multiple MatlabOpaque objects from same file"""
    data = loadmat(pjoin(test_data_path, 'testmatlabstring_7_WIN64.mat'))
    assert "matstring1" in data
    assert isinstance(data['matstring1'], MatlabOpaque)
    assert data['matstring1'][0]['_Class'] == "string"
    assert data['matstring1'][0]['_TypeSystem'] == "MCOS"
    assert data['matstring1'][0]['_ObjectMetadata'].dtype == np.uint32

    assert "matstring2" in data
    assert isinstance(data['matstring2'], MatlabOpaque)
    assert data['matstring2'][0]['_Class'] == "string"
    assert data['matstring2'][0]['_TypeSystem'] == "MCOS"
    assert data['matstring2'][0]['_ObjectMetadata'].dtype == np.uint32

    # Ensure different object IDs
    assert data['matstring1'][0]['_ObjectMetadata'][4, 0] == 1
    assert data['matstring2'][0]['_ObjectMetadata'][4, 0] == 2

