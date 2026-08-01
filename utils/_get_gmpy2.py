
def _get_gmpy2(sympy_ground_types):
    if sympy_ground_types not in ('auto', 'gmpy', 'gmpy2'):
        return None

    gmpy = import_module('gmpy2', min_module_version=_GMPY2_MIN_VERSION,
            module_version_attr='version', module_version_attr_call_args=())

    if sympy_ground_types != 'auto' and gmpy is None:
        warn("gmpy2 library is not installed, switching to 'python' ground types")

    return gmpy

