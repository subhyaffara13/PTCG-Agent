
def test_write_matlab_opaque():
    """Test that we can write a MatlabOpaque object"""
    stream = BytesIO()
    arr = np.empty((1, 1), dtype=mio5p.OPAQUE_DTYPE)
    arr[0, 0]['_Class'] = "string"
    arr[0, 0]['_TypeSystem'] = "MCOS"
    arr[0, 0]['_ObjectMetadata'] = np.array([[0xDD000000, 2, 1, 1, 1, 1]],
                                            dtype=np.uint32)
    arr = MatlabOpaque(arr)
    savemat(stream, {'matstring1': arr})

    stream.seek(0)
    data = loadmat(stream)
    assert "matstring1" in data
    assert isinstance(data['matstring1'], MatlabOpaque)
    assert data['matstring1'][0]['_Class'] == "string"
    assert data['matstring1'][0]['_TypeSystem'] == "MCOS"
    assert data['matstring1'][0]['_ObjectMetadata'].dtype == np.uint32

