
def test_newtons_method_function__ccode():
    x = Symbol('x', real=True)
    expr = cos(x) - x**3
    func = newtons_method_function(expr, x)

    if not cython:
        skip("cython not installed.")
    if not has_c():
        skip("No C compiler found.")

    compile_kw = {"std": 'c99'}
    with tempfile.TemporaryDirectory() as folder:
        mod, info = compile_link_import_strings([
            ('newton.c', ('#include <math.h>\n'
                          '#include <stdio.h>\n') + ccode(func)),
            ('_newton.pyx', ("#cython: language_level={}\n".format("3") +
                             "cdef extern double newton(double)\n"
                             "def py_newton(x):\n"
                             "    return newton(x)\n"))
        ], build_dir=folder, compile_kwargs=compile_kw)
        assert abs(mod.py_newton(0.5) - 0.865474033102) < 1e-12

