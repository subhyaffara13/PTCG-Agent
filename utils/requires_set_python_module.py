
def requires_set_python_module() -> bool:
    """If an op was defined in C++ and extended from Python using the
    torch.library APIs, returns if we require that there have been a
    m.set_python_module("mylib.ops") call from C++ that associates
    the C++ op with a python module.
    """
    return getattr(_utils_internal, "REQUIRES_SET_PYTHON_MODULE", True)

