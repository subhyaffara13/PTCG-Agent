
def get_explicit_native_class(path: str, cdef: ClassDef, errors: Errors) -> bool | None:
    """Return value of @mypyc_attr(native_class=True/False) decorator.

    Look for a @mypyc_attr decorator with native_class=True/False and return
    the value assigned or None if it doesn't exist. Other values are an error.
    """

    for d in cdef.decorators:
        mypyc_attr_call = get_mypyc_attr_call(d)
        if not mypyc_attr_call:
            continue

        for i, name in enumerate(mypyc_attr_call.arg_names):
            if name != "native_class":
                continue

            arg = mypyc_attr_call.args[i]
            if not isinstance(arg, NameExpr):
                errors.error("native_class must be used with True or False only", path, cdef.line)
                return None

            if arg.name == "False":
                return False
            elif arg.name == "True":
                return True
            else:
                errors.error("native_class must be used with True or False only", path, cdef.line)
                return None
    return None

