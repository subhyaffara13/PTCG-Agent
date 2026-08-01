
def test_cython_wrapper_outarg():
    from sympy.core.relational import Equality
    x, y, z = symbols('x,y,z')
    code_gen = CythonCodeWrapper(C99CodeGen())

    routine = make_routine("test", Equality(z, x + y))
    source = get_string(code_gen.dump_pyx, [routine])
    expected = (
        "cdef extern from 'file.h':\n"
        "    void test(double x, double y, double *z)\n"
        "\n"
        "def test_c(double x, double y):\n"
        "\n"
        "    cdef double z = 0\n"
        "    test(x, y, &z)\n"
        "    return z")
    assert source == expected

