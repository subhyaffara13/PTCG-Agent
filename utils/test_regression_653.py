
def test_regression_653():
    # Saving a dictionary with only invalid keys used to raise an error. Now we
    # save this as an empty struct in matlab space.
    sio = BytesIO()
    savemat(sio, {'d':{1:2}}, format='5')
    back = loadmat(sio)['d']
    # Check we got an empty struct equivalent
    assert_equal(back.shape, (1,1))
    assert_equal(back.dtype, np.dtype(object))
    assert_(back[0,0] is None)

