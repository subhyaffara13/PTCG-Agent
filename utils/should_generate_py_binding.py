
def should_generate_py_binding(f: NativeFunction) -> bool:
    # NativeFunctions that are entirely code-generated should not get python bindings
    # because these codegen implementations are often inefficient. A handful of
    # view_copy style ops were exposed accidentally when they were handwritten and now
    # that we are moving them to codegen for bc reasons we need to keep them exposed in
    # python.
    if "generated" in f.tags and "view_copy" not in f.tags:
        return False

    name = cpp.name(f.func)
    for skip_regex in SKIP_PYTHON_BINDINGS:
        if skip_regex.match(name):
            return False

    signature = str(f.func)
    for pattern in SKIP_PYTHON_BINDINGS_SIGNATURES:
        if pattern == signature:
            return False
    return True

