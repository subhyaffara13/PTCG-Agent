
def test_compiled_ccode_with_rewriting():
    if not cython:
        skip("cython not installed.")
    if not has_c():
        skip("No C compiler found.")

    x = Symbol('x')
    about_two = 2**(58/S(117))*3**(97/S(117))*5**(4/S(39))*7**(92/S(117))/S(30)*pi
    # about_two: 1.999999999999581826
    unchanged = 2*exp(x) - about_two
    xval = S(10)**-11
    ref = unchanged.subs(x, xval).n(19) # 2.0418173913673213e-11

    rewritten = optimize(2*exp(x) - about_two, [expm1_opt])

    # Unfortunately, we need to call ``.n()`` on our expressions before we hand them
    # to ``ccode``, and we need to request a large number of significant digits.
    # In this test, results converged for double precision when the following number
    # of significant digits were chosen:
    NUMBER_OF_DIGITS = 25   # TODO: this should ideally be automatically handled.

    func_c = '''
#include <math.h>

double func_unchanged(double x) {
    return %(unchanged)s;
}
double func_rewritten(double x) {
    return %(rewritten)s;
}
''' % {"unchanged": ccode(unchanged.n(NUMBER_OF_DIGITS)),
           "rewritten": ccode(rewritten.n(NUMBER_OF_DIGITS))}

    func_pyx = '''
#cython: language_level=3
cdef extern double func_unchanged(double)
cdef extern double func_rewritten(double)
def py_unchanged(x):
    return func_unchanged(x)
def py_rewritten(x):
    return func_rewritten(x)
'''
    with tempfile.TemporaryDirectory() as folder:
        mod, info = compile_link_import_strings(
            [('func.c', func_c), ('_func.pyx', func_pyx)],
            build_dir=folder, compile_kwargs={"std": 'c99'}
        )
        err_rewritten = abs(mod.py_rewritten(1e-11) - ref)
        err_unchanged = abs(mod.py_unchanged(1e-11) - ref)
        assert 1e-27 < err_rewritten < 1e-25  # highly accurate.
        assert 1e-19 < err_unchanged < 1e-16  # quite poor.

