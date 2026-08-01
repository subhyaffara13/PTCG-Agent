
def nameprep(s: Any) -> None:
    """Stub for :rfc:`3491` Nameprep, which is not used by IDNA 2008.

    IDNA 2008 (:rfc:`5891`) replaces Nameprep with the per-codepoint
    validity classes from :rfc:`5892`; this function exists only to
    return a clear error if legacy code attempts to call it.

    :raises NotImplementedError: Always.
    """
    raise NotImplementedError("IDNA 2008 does not utilise nameprep protocol")


def nameprep(s: Any) -> None:
    raise NotImplementedError("IDNA 2008 does not utilise nameprep protocol")

