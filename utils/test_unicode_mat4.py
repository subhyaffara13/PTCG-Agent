
def test_unicode_mat4():
    # Mat4 should save unicode as latin1
    bio = BytesIO()
    var = {'second_cat': 'Schrödinger'}
    savemat(bio, var, format='4')
    var_back = loadmat(bio)
    assert_equal(var_back['second_cat'], var['second_cat'])

