
def _attach_print_methods(cls, cont):
    for sympy_name, cxx_name in cont[cls.standard].items():
        _attach_print_method(cls, sympy_name, cxx_name)

