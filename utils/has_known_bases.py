
def has_known_bases(klass, context: InferenceContext | None = None) -> bool:
    """Return whether all base classes of a class could be inferred."""
    try:
        return klass._all_bases_known
    except AttributeError:
        pass
    for base in klass.bases:
        result = real_safe_infer(base, context=context)
        # TODO: check for A->B->A->B pattern in class structure too?
        if (
            not isinstance(result, scoped_nodes.ClassDef)
            or result is klass
            or not has_known_bases(result, context=context)
        ):
            klass._all_bases_known = False
            return False
    klass._all_bases_known = True
    return True


def has_known_bases(
    klass: nodes.ClassDef, context: InferenceContext | None = None
) -> bool:
    """Return true if all base classes of a class could be inferred."""
    try:
        return klass._all_bases_known  # type: ignore[no-any-return]
    except AttributeError:
        pass
    for base in klass.bases:
        result = safe_infer(base, context=context)
        if (
            not isinstance(result, nodes.ClassDef)
            or result is klass
            or not has_known_bases(result, context=context)
        ):
            klass._all_bases_known = False
            return False
    klass._all_bases_known = True
    return True

