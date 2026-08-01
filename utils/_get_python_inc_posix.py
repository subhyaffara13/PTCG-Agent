
def _get_python_inc_posix(prefix, spec_prefix, plat_specific):
    return (
        _get_python_inc_posix_python(plat_specific)
        or _extant(_get_python_inc_from_config(plat_specific, spec_prefix))
        or _get_python_inc_posix_prefix(prefix)
    )

