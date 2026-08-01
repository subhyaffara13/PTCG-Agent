
def test_write_multiple_matlab_opaque():
    """Round-trip two MatlabOpaque objects with distinct IDs in one mdict."""
    def make_opaque(obj_id):
        arr = np.empty((1, 1), dtype=mio5p.OPAQUE_DTYPE)
        arr[0, 0]['_Class'] = "string"
        arr[0, 0]['_TypeSystem'] = "MCOS"
        arr[0, 0]['_ObjectMetadata'] = np.array(
            [[0xDD000000], [2], [1], [1], [obj_id], [1]], dtype=np.uint32)
        return MatlabOpaque(arr)

    stream = BytesIO()
    savemat(stream, {'matstring1': make_opaque(1),
                     'matstring2': make_opaque(2)})
    stream.seek(0)
    data = loadmat(stream)
    for name, expected_id in [('matstring1', 1), ('matstring2', 2)]:
        assert name in data
        assert isinstance(data[name], MatlabOpaque)
        assert data[name][0]['_Class'] == "string"
        assert data[name][0]['_TypeSystem'] == "MCOS"
        assert data[name][0]['_ObjectMetadata'].dtype == np.uint32
        assert data[name][0]['_ObjectMetadata'][4, 0] == expected_id

