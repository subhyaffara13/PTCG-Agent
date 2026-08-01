
def test_scalar_squeeze():
    stream = BytesIO()
    in_d = {'scalar': [[0.1]], 'string': 'my name', 'st':{'one':1, 'two':2}}
    savemat(stream, in_d)
    out_d = loadmat(stream, squeeze_me=True)
    assert_(isinstance(out_d['scalar'], float))
    assert_(isinstance(out_d['string'], str))
    assert_(isinstance(out_d['st'], np.ndarray))

