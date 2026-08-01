
def ep_matches(ep: EntryPoint, **params) -> bool:
    """
    Workaround for ``EntryPoint`` objects without the ``matches`` method.
    """
    try:
        return ep.matches(**params)
    except AttributeError:
        from .. import EntryPoint  # -> delay to prevent circular imports.

        # Reconstruct the EntryPoint object to make sure it is compatible.
        return EntryPoint(ep.name, ep.value, ep.group).matches(**params)

