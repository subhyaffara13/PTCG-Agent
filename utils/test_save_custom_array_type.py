import os

def test_save_custom_array_type(tmpdir):
    class CustomArray:
        def __array__(self, dtype=None, copy=None):
            return np.arange(6.0).reshape(2, 3)
    a = CustomArray()
    filename = os.path.join(str(tmpdir), 'test.mat')
    savemat(filename, {'a': a})
    out = loadmat(filename)
    assert_array_equal(out['a'], np.array(a))

