
def validate_modulename(pyf_files, modulename='untitled'):
    if len(pyf_files) > 1:
        raise ValueError("Only one .pyf file per call")
    if pyf_files:
        pyff = pyf_files[0]
        pyf_modname = auxfuncs.get_f2py_modulename(pyff)
        if modulename != pyf_modname:
            outmess(
                f"Ignoring -m {modulename}.\n"
                f"{pyff} defines {pyf_modname} to be the modulename.\n"
            )
            modulename = pyf_modname
    return modulename

