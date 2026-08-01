
def _get_dependency_info() -> dict[str, JSONSerializable]:
    """
    Returns dependency information as a JSON serializable dictionary.
    """
    deps = [
        "pandas",
        # required
        "numpy",
        "dateutil",
        # install / build,
        "pip",
        "Cython",
        # docs
        "sphinx",
        # Other, not imported.
        "IPython",
    ]
    # Optional dependencies
    deps.extend(list(VERSIONS))

    result: dict[str, JSONSerializable] = {}
    for modname in deps:
        try:
            mod = import_optional_dependency(modname, errors="ignore")
        except Exception:
            # Dependency conflicts may cause a non ImportError
            result[modname] = "N/A"
        else:
            result[modname] = get_version(mod) if mod else None
    return result

