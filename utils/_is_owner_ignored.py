
def _is_owner_ignored(
    owner: SuccessfulInferenceResult,
    attrname: str | None,
    ignored_classes: Iterable[str],
    ignored_modules: Iterable[str],
) -> bool:
    """Check if the given owner should be ignored.

    This will verify if the owner's module is in *ignored_modules*
    or the owner's module fully qualified name is in *ignored_modules*
    or if the *ignored_modules* contains a pattern which catches
    the fully qualified name of the module.

    Also, similar checks are done for the owner itself, if its name
    matches any name from the *ignored_classes* or if its qualified
    name can be found in *ignored_classes*.
    """
    if is_module_ignored(owner.root().qname(), ignored_modules):
        return True

    # Match against ignored classes.
    ignored_classes = set(ignored_classes)
    qname = owner.qname() if hasattr(owner, "qname") else ""
    return any(ignore in (attrname, qname) for ignore in ignored_classes)

