import re

def safe_extra(extra: str) -> NormalizedExtra:
    """Convert an arbitrary string to a standard 'extra' name

    Any runs of non-alphanumeric characters are replaced with a single '_',
    and the result is always lowercased.

    This function is duplicated from ``pkg_resources``. Note that this is not
    the same to either ``canonicalize_name`` or ``_egg_link_name``.
    """
    return cast(NormalizedExtra, re.sub("[^A-Za-z0-9.-]+", "_", extra).lower())


def safe_extra(extra: str) -> str:
    """Convert an arbitrary string to a standard 'extra' name

    Any runs of non-alphanumeric characters are replaced with a single '_',
    and the result is always lowercased.
    """
    return re.sub('[^A-Za-z0-9.-]+', '_', extra).lower()


def safe_extra(extra: str) -> str:
    """Normalize extra name according to PEP 685
    >>> safe_extra("_FrIeNdLy-._.-bArD")
    'friendly-bard'
    >>> safe_extra("FrIeNdLy-._.-bArD__._-")
    'friendly-bard'
    """
    return _NON_ALPHANUMERIC.sub("-", extra).strip("-").lower()


def safe_extra(extra: str) -> str:
    """Convert an arbitrary string to a standard 'extra' name
    Any runs of non-alphanumeric characters are replaced with a single '_',
    and the result is always lowercased.
    """
    return re.sub("[^A-Za-z0-9.-]+", "_", extra).lower()

