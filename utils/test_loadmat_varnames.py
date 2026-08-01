
def test_loadmat_varnames():
    # Test that we can get just one variable from a mat file using loadmat
    mat5_sys_names = ['__globals__',
                      '__header__',
                      '__version__']
    for eg_file, sys_v_names in (
        (pjoin(test_data_path, 'testmulti_4.2c_SOL2.mat'), []), (pjoin(
            test_data_path, 'testmulti_7.4_GLNX86.mat'), mat5_sys_names)):
        vars = loadmat(eg_file)
        assert_equal(set(vars.keys()), set(['a', 'theta'] + sys_v_names))
        vars = loadmat(eg_file, variable_names='a')
        assert_equal(set(vars.keys()), set(['a'] + sys_v_names))
        vars = loadmat(eg_file, variable_names=['a'])
        assert_equal(set(vars.keys()), set(['a'] + sys_v_names))
        vars = loadmat(eg_file, variable_names=['theta'])
        assert_equal(set(vars.keys()), set(['theta'] + sys_v_names))
        vars = loadmat(eg_file, variable_names=('theta',))
        assert_equal(set(vars.keys()), set(['theta'] + sys_v_names))
        vars = loadmat(eg_file, variable_names=[])
        assert_equal(set(vars.keys()), set(sys_v_names))
        vnames = ['theta']
        vars = loadmat(eg_file, variable_names=vnames)
        assert_equal(vnames, ['theta'])

