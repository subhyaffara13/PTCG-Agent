
def _make_source(name, init, body):
    """ Combines the code fragments into source code ready to be compiled
    """
    code = f"""
    #include <Python.h>

    {body}

    PyMODINIT_FUNC
    PyInit_{name}(void) {{
    {init}
    }}
    """
    return code

