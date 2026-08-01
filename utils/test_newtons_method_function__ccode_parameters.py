
def test_newtons_method_function__ccode_parameters():
    args = x, A, k, p = symbols('x A k p')
    expr = A*cos(k*x) - p*x**3
    raises(ValueError, lambda: newtons_method_function(expr, x))
    use_wurlitzer = wurlitzer

    func = newtons_method_function(expr, x, args, debug=use_wurlitzer)

    if not has_c():
        skip("No C compiler found.")
    if not cython:
        skip("cython not installed.")

    compile_kw = {"std": 'c99'}
    with tempfile.TemporaryDirectory() as folder:
        mod, info = compile_link_import_strings([
            ('newton_par.c', ('#include <math.h>\n'
                          '#include <stdio.h>\n') + ccode(func)),
            ('_newton_par.pyx', ("#cython: language_level={}\n".format("3") +
                                 "cdef extern double newton(double, double, double, double)\n"
                             "def py_newton(x, A=1, k=1, p=1):\n"
                             "    return newton(x, A, k, p)\n"))
        ], compile_kwargs=compile_kw, build_dir=folder)

        if use_wurlitzer:
            with wurlitzer.pipes() as (out, err):
                result = mod.py_newton(0.5)
        else:
            result = mod.py_newton(0.5)

        assert abs(result - 0.865474033102) < 1e-12

        if not use_wurlitzer:
            skip("C-level output only tested when package 'wurlitzer' is available.")

        out, err = out.read(), err.read()
        assert err == ''
        assert out == """\
x=         0.5
x=      1.1121 d_x=     0.61214
x=     0.90967 d_x=    -0.20247
x=     0.86726 d_x=   -0.042409
x=     0.86548 d_x=  -0.0017867
x=     0.86547 d_x= -3.1022e-06
x=     0.86547 d_x= -9.3421e-12
x=     0.86547 d_x=  3.6902e-17
"""  # try to run tests with LC_ALL=C if this assertion fails

