
def _get_python_inc_nt(prefix, spec_prefix, plat_specific):
    if python_build:
        # Include both include dirs to ensure we can find pyconfig.h
        return (
            os.path.join(prefix, "include")
            + os.path.pathsep
            + os.path.dirname(sysconfig.get_config_h_filename())
        )
    return os.path.join(prefix, "include")

