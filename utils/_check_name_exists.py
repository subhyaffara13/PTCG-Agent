
def _check_name_exists(ns: str | None, name: str):
    """Check if an env exists in a namespace. If it doesn't, print a helpful error message."""
    # First check if the namespace exists
    _check_namespace_exists(ns)

    # Then check if the name exists
    names: set[str] = {
        env_spec.name for env_spec in registry.values() if env_spec.namespace == ns
    }
    if name in names:
        return

    # Otherwise, raise a helpful error to the user
    suggestion = difflib.get_close_matches(name, names, n=1)
    namespace_msg = f" in namespace {ns}" if ns else ""
    suggestion_msg = f" Did you mean: `{suggestion[0]}`?" if suggestion else ""

    raise error.NameNotFound(
        f"Environment `{name}` doesn't exist{namespace_msg}.{suggestion_msg}"
    )


def _check_name_exists(ns: Optional[str], name: str):
    """Check if an env exists in a namespace. If it doesn't, print a helpful error message."""
    _check_namespace_exists(ns)
    names = {spec_.name for spec_ in registry.values() if spec_.namespace == ns}

    if name in names:
        return

    suggestion = difflib.get_close_matches(name, names, n=1)
    namespace_msg = f" in namespace {ns}" if ns else ""
    suggestion_msg = f"Did you mean: `{suggestion[0]}`?" if suggestion else ""

    raise error.NameNotFound(
        f"Environment {name} doesn't exist{namespace_msg}. {suggestion_msg}"
    )

