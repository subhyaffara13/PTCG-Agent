
def test_single_object():
    stream = BytesIO()
    savemat(stream, {'A':np.array(1, dtype=object)})

