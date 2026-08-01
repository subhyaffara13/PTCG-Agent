
def test_load_mat4_le():
    # We were getting byte order wrong when reading little-endian floa64 dense
    # matrices on big-endian platforms
    mat4_fname = pjoin(test_data_path, 'test_mat4_le_floats.mat')
    vars = loadmat(mat4_fname)
    assert_array_equal(vars['a'], [[0.1, 1.2]])

