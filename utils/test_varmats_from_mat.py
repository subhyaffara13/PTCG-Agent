
def test_varmats_from_mat():
    # Make a mat file with several variables, write it, read it back
    names_vars = (('arr', mlarr(np.arange(10))),
                  ('mystr', mlarr('a string')),
                  ('mynum', mlarr(10)))

    # Dict like thing to give variables in defined order
    class C:
        def items(self):
            return names_vars
    stream = BytesIO()
    savemat(stream, C())
    varmats = varmats_from_mat(stream)
    assert_equal(len(varmats), 3)
    for i in range(3):
        name, var_stream = varmats[i]
        exp_name, exp_res = names_vars[i]
        assert_equal(name, exp_name)
        res = loadmat(var_stream)
        assert_array_equal(res[name], exp_res)

