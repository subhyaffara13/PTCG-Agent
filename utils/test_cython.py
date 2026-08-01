
def test_cython(tmp_path):
    srcdir = os.path.dirname(os.path.dirname(__file__))
    extensions, extensions_cpp = _test_cython_extension(tmp_path, srcdir)
    # actually test the cython c-extensions
    assert extensions.cy_beta(0.5, 0.1) == beta(0.5, 0.1)
    assert extensions.cy_gamma(0.5 + 1.0j) == gamma(0.5 + 1.0j)
    assert extensions_cpp.cy_beta(0.5, 0.1) == beta(0.5, 0.1)
    assert extensions_cpp.cy_gamma(0.5 + 1.0j) == gamma(0.5 + 1.0j)


def test_cython(tmp_path):
    srcdir = os.path.dirname(os.path.dirname(__file__))
    extensions, extensions_cpp = _test_cython_extension(tmp_path, srcdir)
    # actually test the cython c-extensions
    # From docstring for scipy.optimize.cython_optimize module
    x = extensions.brentq_example()
    assert x == 0.6999942848231314
    x = extensions_cpp.brentq_example()
    assert x == 0.6999942848231314


def test_cython(tmp_path):
    srcdir = os.path.dirname(os.path.dirname(__file__))
    extensions, extensions_cpp = _test_cython_extension(tmp_path, srcdir)
    # actually test the cython c-extensions
    a = np.ones(8) * 3
    b = np.ones(9)
    c = np.ones(8) * 4
    x = np.ones(9)
    dgtsv = get_lapack_funcs('gtsv', dtype=np.float64, ilp64="preferred")
    _, _, _, x, _ = dgtsv(a, b, c, x)
    a = np.ones(8) * 3
    b = np.ones(9)
    c = np.ones(8) * 4
    x_c = np.ones(9)
    extensions.tridiag(a, b, c, x_c)
    a = np.ones(8) * 3
    b = np.ones(9)
    c = np.ones(8) * 4
    x_cpp = np.ones(9)
    extensions_cpp.tridiag(a, b, c, x_cpp)
    np.testing.assert_array_equal(x, x_cpp)
    cx = np.array([1-1j, 2+2j, 3-3j], dtype=np.complex64)
    cy = np.array([4+4j, 5-5j, 6+6j], dtype=np.complex64)
    cdotu = get_blas_funcs('dotu', dtype=np.complex64, ilp64="preferred")
    np.testing.assert_array_equal(cdotu(cx, cy), extensions.complex_dot(cx, cy))
    np.testing.assert_array_equal(cdotu(cx, cy), extensions_cpp.complex_dot(cx, cy))

    # Verify blas_int size consistency between installed and JIT-compiled modules
    expected_size = cython_blas._blas_int_size()
    assert extensions.get_blas_int_size() == expected_size
    assert extensions_cpp.get_blas_int_size() == expected_size


def test_cython(tmp_path):
    import glob
    # build the examples in a temporary directory
    srcdir = os.path.join(os.path.dirname(__file__), '..')
    shutil.copytree(srcdir, tmp_path / 'random')
    build_dir = tmp_path / 'random' / '_examples' / 'cython'
    target_dir = build_dir / "build"
    os.makedirs(target_dir, exist_ok=True)
    # Ensure we use the correct Python interpreter even when `meson` is
    # installed in a different Python environment (see gh-24956)
    native_file = str(build_dir / 'interpreter-native-file.ini')
    with open(native_file, 'w') as f:
        f.write("[binaries]\n")
        f.write(f"python = '{sys.executable}'\n")
        f.write(f"python3 = '{sys.executable}'")
    if sys.platform == "win32":
        run_subprocess(["meson", "setup",
                        "--buildtype=release",
                        "--vsenv", "--native-file", native_file,
                        str(build_dir)],
                       target_dir)
    else:
        run_subprocess(["meson", "setup",
                        "--native-file", native_file, str(build_dir)],
                       target_dir)
    run_subprocess(["meson", "compile", "-vv"], target_dir)

    # gh-16162: make sure numpy's __init__.pxd was used for cython
    # not really part of this test, but it is a convenient place to check

    g = glob.glob(str(target_dir / "*" / "extending.pyx.c"))
    with open(g[0]) as fid:
        txt_to_find = 'NumPy API declarations from "numpy/__init__'
        for line in fid:
            if txt_to_find in line:
                break
        else:
            assert False, f"Could not find '{txt_to_find}' in C file, wrong pxd used"
    # import without adding the directory to sys.path
    suffix = sysconfig.get_config_var('EXT_SUFFIX')

    def load(modname):
        so = (target_dir / modname).with_suffix(suffix)
        spec = spec_from_file_location(modname, so)
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    # test that the module can be imported
    load("extending")
    load("extending_cpp")
    # actually test the cython c-extension
    extending_distributions = load("extending_distributions")
    from numpy.random import PCG64
    values = extending_distributions.uniforms_ex(PCG64(0), 10, 'd')
    assert values.shape == (10,)
    assert values.dtype == np.float64

