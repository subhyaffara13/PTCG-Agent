
def test_cython_wrapper_scalar_function():
    x, y, z = symbols('x,y,z')
    expr = (x + y)*z
    routine = make_routine("test", expr)
    code_gen = CythonCodeWrapper(CCodeGen())
    source = get_string(code_gen.dump_pyx, [routine])

    expected = (
        "cdef extern from 'file.h':\n"
        "    double test(double x, double y, double z)\n"
        "\n"
        "def test_c(double x, double y, double z):\n"
        "\n"
        "    return test(x, y, z)")
    assert source == expected

