
def fixup_id(value: str) -> Optional[str]:
    """Fixup SPDX-ID.

    :returns: repaired value string, or `None` if fixup was unable to help.
    """
    return __IDS_LOWER_MAP.get(value.lower())

