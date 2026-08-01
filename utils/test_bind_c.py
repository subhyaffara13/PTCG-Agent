
def test_bind_C():
    if not has_fortran():
        skip("No fortran compiler found.")
    if not cython:
        skip("Cython not found.")
    if not np:
        skip("NumPy not found.")

    a = Symbol('a', real=True)
    s = Symbol('s', integer=True)
    body = [Return((sum_(a**2)/s)**.5)]
    arr = array(a, dim=[s], intent='in')
    fd = FunctionDefinition(real, 'rms', [arr, s], body, attrs=[bind_C('rms')])
    f_mod = render_as_module([fd], 'mod_rms')

    with tempfile.TemporaryDirectory() as folder:
        mod, info = compile_link_import_strings([
            ('rms.f90', f_mod),
            ('_rms.pyx', (
                "#cython: language_level={}\n".format("3") +
                "cdef extern double rms(double*, int*)\n"
                "def py_rms(double[::1] x):\n"
                "    cdef int s = x.size\n"
                "    return rms(&x[0], &s)\n"))
        ], build_dir=folder)
        assert abs(mod.py_rms(np.array([2., 4., 2., 2.])) - 7**0.5) < 1e-14

