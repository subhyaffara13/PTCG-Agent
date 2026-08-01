
def _make_methods(functions, modname):
    """ Turns the name, signature, code in functions into complete functions
    and lists them in a methods_table. Then turns the methods_table into a
    ``PyMethodDef`` structure and returns the resulting code fragment ready
    for compilation
    """
    methods_table = []
    codes = []
    for funcname, flags, code in functions:
        cfuncname = f"{modname}_{funcname}"
        if 'METH_KEYWORDS' in flags:
            signature = '(PyObject *self, PyObject *args, PyObject *kwargs)'
        else:
            signature = '(PyObject *self, PyObject *args)'
        methods_table.append(f'{{"{funcname}", (PyCFunction){cfuncname}, {flags}}},')
        func_code = f"""
        static PyObject* {cfuncname}{signature}
        {{
        {code}
        }}
        """
        codes.append(func_code)

    methods_str = '\n'.join(methods_table)
    body = "\n".join(codes) + f"""
    static PyMethodDef methods[] = {{
    {methods_str}
    {{ NULL }}
    }};
    static struct PyModuleDef moduledef = {{
        PyModuleDef_HEAD_INIT,
        "{modname}",    /* m_name */
        NULL,           /* m_doc */
        -1,             /* m_size */
        methods,        /* m_methods */
    }};
    """
    return body

