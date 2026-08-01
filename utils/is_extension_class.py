
def is_extension_class(path: str, cdef: ClassDef, errors: Errors) -> bool:
    # Check for @mypyc_attr(native_class=True/False) decorator.
    explicit_native_class = get_explicit_native_class(path, cdef, errors)

    # Classes with native_class=False are explicitly marked as non extension.
    if explicit_native_class is False:
        return False

    implicit_extension_class, reason = is_implicit_extension_class(cdef)

    # Classes with native_class=True should be extension classes, but they might
    # not be able to be due to other reasons. Print an error in that case.
    if explicit_native_class is True and not implicit_extension_class:
        errors.error(
            f"Class is marked as native_class=True but it can't be a native class. {reason}",
            path,
            cdef.line,
        )

    return implicit_extension_class

