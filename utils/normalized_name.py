
def normalized_name(dist: Distribution) -> str | None:
    """
    Honor name normalization for distributions that don't provide ``_normalized_name``.
    """
    try:
        return dist._normalized_name
    except AttributeError:
        from .. import Prepared  # -> delay to prevent circular imports.

        return Prepared.normalize(
            getattr(dist, "name", None) or md_none(dist.metadata)['Name']
        )

