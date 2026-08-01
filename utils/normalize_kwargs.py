
def normalize_kwargs(kw, alias_mapping=None):
    """
    Helper function to normalize kwarg inputs.

    Parameters
    ----------
    kw : dict or None
        A dict of keyword arguments.  None is explicitly supported and treated
        as an empty dict, to support functions with an optional parameter of
        the form ``props=None``.

    alias_mapping : Artist subclass or Artist instance
        A mapping between a canonical name to a list of aliases, in order of
        precedence from lowest to highest.

        If the canonical value is not in the list it is assumed to have the
        highest priority.

        If an Artist subclass or instance is passed, use its properties alias
        mapping.

    Raises
    ------
    TypeError
        To match what Python raises if invalid arguments/keyword arguments are
        passed to a callable.
    """
    from matplotlib.artist import Artist

    # deal with default value of alias_mapping
    if (isinstance(alias_mapping, type) and issubclass(alias_mapping, Artist)
          or isinstance(alias_mapping, Artist)):
        alias_to_prop = getattr(alias_mapping, "_alias_to_prop", {})
    else:
        if alias_mapping is None:
            alias_mapping = {}
        _api.warn_deprecated("3.11", message=(
            "Passing a dict or None as alias_mapping to normalize_kwargs is "
            "deprecated since %(since)s and support will be removed "
            "%(removal)s; pass an Artist instance or type instead."))
        # Convert old format to new format.
        alias_to_prop = {alias: prop for prop, aliases in alias_mapping.items()
                         for alias in aliases}

    if kw is None:
        return {}

    canonicalized = {alias_to_prop.get(k, k): v for k, v in kw.items()}
    if len(canonicalized) == len(kw):
        return canonicalized

    canonical_to_seen = {}
    for k in kw:
        canonical = alias_to_prop.get(k, k)
        if canonical in canonical_to_seen:
            raise TypeError(f"Got both {canonical_to_seen[canonical]!r} and "
                            f"{k!r}, which are aliases of one another")
        canonical_to_seen[canonical] = k

