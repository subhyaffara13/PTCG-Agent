
def test_ufuncify_source():
    x, y, z = symbols('x,y,z')
    code_wrapper = UfuncifyCodeWrapper(C99CodeGen("ufuncify"))
    routine = make_routine("test", x + y + z)
    source = get_string(code_wrapper.dump_c, [routine])
    expected = """\
#include "Python.h"
#include "math.h"
#include "numpy/ndarraytypes.h"
#include "numpy/ufuncobject.h"
#include "numpy/halffloat.h"
#include "file.h"

static PyMethodDef wrapper_module_%(num)sMethods[] = {
        {NULL, NULL, 0, NULL}
};

#ifdef NPY_1_19_API_VERSION
static void test_ufunc(char **args, const npy_intp *dimensions, const npy_intp* steps, void* data)
#else
static void test_ufunc(char **args, npy_intp *dimensions, npy_intp* steps, void* data)
#endif
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char *in0 = args[0];
    char *in1 = args[1];
    char *in2 = args[2];
    char *out0 = args[3];
    npy_intp in0_step = steps[0];
    npy_intp in1_step = steps[1];
    npy_intp in2_step = steps[2];
    npy_intp out0_step = steps[3];
    for (i = 0; i < n; i++) {
        *((double *)out0) = test(*(double *)in0, *(double *)in1, *(double *)in2);
        in0 += in0_step;
        in1 += in1_step;
        in2 += in2_step;
        out0 += out0_step;
    }
}
PyUFuncGenericFunction test_funcs[1] = {&test_ufunc};
static char test_types[4] = {NPY_DOUBLE, NPY_DOUBLE, NPY_DOUBLE, NPY_DOUBLE};
static void *test_data[1] = {NULL};

#if PY_VERSION_HEX >= 0x03000000
static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "wrapper_module_%(num)s",
    NULL,
    -1,
    wrapper_module_%(num)sMethods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC PyInit_wrapper_module_%(num)s(void)
{
    PyObject *m, *d;
    PyObject *ufunc0;
    m = PyModule_Create(&moduledef);
    if (!m) {
        return NULL;
    }
    import_array();
    import_umath();
    d = PyModule_GetDict(m);
    ufunc0 = PyUFunc_FromFuncAndData(test_funcs, test_data, test_types, 1, 3, 1,
            PyUFunc_None, "wrapper_module_%(num)s", "Created in SymPy with Ufuncify", 0);
    PyDict_SetItemString(d, "test", ufunc0);
    Py_DECREF(ufunc0);
    return m;
}
#else
PyMODINIT_FUNC initwrapper_module_%(num)s(void)
{
    PyObject *m, *d;
    PyObject *ufunc0;
    m = Py_InitModule("wrapper_module_%(num)s", wrapper_module_%(num)sMethods);
    if (m == NULL) {
        return;
    }
    import_array();
    import_umath();
    d = PyModule_GetDict(m);
    ufunc0 = PyUFunc_FromFuncAndData(test_funcs, test_data, test_types, 1, 3, 1,
            PyUFunc_None, "wrapper_module_%(num)s", "Created in SymPy with Ufuncify", 0);
    PyDict_SetItemString(d, "test", ufunc0);
    Py_DECREF(ufunc0);
}
#endif""" % {'num': CodeWrapper._module_counter}
    assert source == expected

