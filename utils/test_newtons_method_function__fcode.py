
def test_newtons_method_function__fcode():
    x = Symbol('x', real=True)
    expr = cos(x) - x**3
    func = newtons_method_function(expr, x, attrs=[bind_C(name='newton')])

    if not cython:
        skip("cython not installed.")
    if not has_fortran():
        skip("No Fortran compiler found.")

    f_mod = f_module([func], 'mod_newton')
    with tempfile.TemporaryDirectory() as folder:
        mod, info = compile_link_import_strings([
            ('newton.f90', f_mod),
            ('_newton.pyx', ("#cython: language_level={}\n".format("3") +
                             "cdef extern double newton(double*)\n"
                             "def py_newton(double x):\n"
                             "    return newton(&x)\n"))
        ], build_dir=folder)
        assert abs(mod.py_newton(0.5) - 0.865474033102) < 1e-12

