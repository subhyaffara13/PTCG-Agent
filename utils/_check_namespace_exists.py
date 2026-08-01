
def _check_namespace_exists(ns: str | None):
    """Check if a namespace exists. If it doesn't, print a helpful error message."""
    # If the namespace is none, then the namespace does exist
    if ns is None:
        return

    # Check if the namespace exists in one of the registry's specs
    namespaces: set[str] = {
        env_spec.namespace
        for env_spec in registry.values()
        if env_spec.namespace is not None
    }
    if ns in namespaces:
        return

    # Otherwise, the namespace doesn't exist and raise a helpful message
    suggestion = (
        difflib.get_close_matches(ns, namespaces, n=1) if len(namespaces) > 0 else None
    )
    if suggestion:
        suggestion_msg = f"Did you mean: `{suggestion[0]}`?"
    else:
        suggestion_msg = f"Have you installed the proper package for {ns}?"

    raise error.NamespaceNotFound(f"Namespace {ns} not found. {suggestion_msg}")


def _check_namespace_exists(ns: Optional[str]):
    """Check if a namespace exists. If it doesn't, print a helpful error message."""
    if ns is None:
        return
    namespaces = {
        spec_.namespace for spec_ in registry.values() if spec_.namespace is not None
    }
    if ns in namespaces:
        return

    suggestion = (
        difflib.get_close_matches(ns, namespaces, n=1) if len(namespaces) > 0 else None
    )
    suggestion_msg = (
        f"Did you mean: `{suggestion[0]}`?"
        if suggestion
        else f"Have you installed the proper package for {ns}?"
    )

    raise error.NamespaceNotFound(f"Namespace {ns} not found. {suggestion_msg}")

