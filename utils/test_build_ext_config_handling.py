
def test_build_ext_config_handling(tmpdir_cwd):
    files = {
        'setup.py': DALS(
            """
            from setuptools import Extension, setup
            setup(
                name='foo',
                version='0.0.0',
                ext_modules=[Extension('foo', ['foo.c'])],
            )
            """
        ),
        'foo.c': DALS(
            """
            #include "Python.h"

            #if PY_MAJOR_VERSION >= 3

            static struct PyModuleDef moduledef = {
                    PyModuleDef_HEAD_INIT,
                    "foo",
                    NULL,
                    0,
                    NULL,
                    NULL,
                    NULL,
                    NULL,
                    NULL
            };

            #define INITERROR return NULL

            PyMODINIT_FUNC PyInit_foo(void)

            #else

            #define INITERROR return

            void initfoo(void)

            #endif
            {
            #if PY_MAJOR_VERSION >= 3
                PyObject *module = PyModule_Create(&moduledef);
            #else
                PyObject *module = Py_InitModule("extension", NULL);
            #endif
                if (module == NULL)
                    INITERROR;
            #if PY_MAJOR_VERSION >= 3
                return module;
            #endif
            }
            """
        ),
        'setup.cfg': DALS(
            """
            [build]
            build_base = foo_build
            """
        ),
    }
    path.build(files)
    code, (stdout, stderr) = environment.run_setup_py(
        cmd=['build'],
        data_stream=(0, 2),
    )
    assert code == 0, f'\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}'

