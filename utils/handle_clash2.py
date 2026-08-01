
def handleClash2(existing=[], prefix="", suffix=""):
    """
    existing should be a case-insensitive list
    of all existing file names.

    >>> prefix = ("0" * 5) + "."
    >>> suffix = "." + ("0" * 10)
    >>> existing = [prefix + str(i) + suffix for i in range(100)]

    >>> e = list(existing)
    >>> handleClash2(existing=e, prefix=prefix, suffix=suffix) == (
    ... 	'00000.100.0000000000')
    True

    >>> e = list(existing)
    >>> e.remove(prefix + "1" + suffix)
    >>> handleClash2(existing=e, prefix=prefix, suffix=suffix) == (
    ... 	'00000.1.0000000000')
    True

    >>> e = list(existing)
    >>> e.remove(prefix + "2" + suffix)
    >>> handleClash2(existing=e, prefix=prefix, suffix=suffix) == (
    ... 	'00000.2.0000000000')
    True
    """
    # calculate the longest possible string
    maxLength = maxFileNameLength - len(prefix) - len(suffix)
    maxValue = int("9" * maxLength)
    # try to find a number
    finalName = None
    counter = 1
    while finalName is None:
        fullName = prefix + str(counter) + suffix
        if fullName.lower() not in existing:
            finalName = fullName
            break
        else:
            counter += 1
        if counter >= maxValue:
            break
    # raise an error if nothing has been found
    if finalName is None:
        raise NameTranslationError("No unique name could be found.")
    # finished
    return finalName


def handleClash2(
    existing: Iterable[str] = [], prefix: str = "", suffix: str = ""
) -> str:
    """A helper function that resolves collisions with existing names when choosing a filename.

    This function is a fallback to :func:`handleClash1`. It attempts to append an unused integer counter to the filename.

        Args:
                userName (str): The input file name.
                existing: A case-insensitive list of all existing file names.
                prefix: Prefix to be prepended to the file name.
                suffix: Suffix to be appended to the file name.

        Returns:
                A suitable filename.

        Raises:
                NameTranslationError: If no suitable name could be generated.

        Examples::

          >>> prefix = ("0" * 5) + "."
          >>> suffix = "." + ("0" * 10)
          >>> existing = [prefix + str(i) + suffix for i in range(100)]

          >>> e = list(existing)
          >>> handleClash2(existing=e, prefix=prefix, suffix=suffix) == (
          ... 	'00000.100.0000000000')
          True

          >>> e = list(existing)
          >>> e.remove(prefix + "1" + suffix)
          >>> handleClash2(existing=e, prefix=prefix, suffix=suffix) == (
          ... 	'00000.1.0000000000')
          True

          >>> e = list(existing)
          >>> e.remove(prefix + "2" + suffix)
          >>> handleClash2(existing=e, prefix=prefix, suffix=suffix) == (
          ... 	'00000.2.0000000000')
          True
    """
    # calculate the longest possible string
    maxLength = maxFileNameLength - len(prefix) - len(suffix)
    maxValue = int("9" * maxLength)
    # try to find a number
    finalName = None
    counter = 1
    while finalName is None:
        fullName = prefix + str(counter) + suffix
        if fullName.lower() not in existing:
            finalName = fullName
            break
        else:
            counter += 1
        if counter >= maxValue:
            break
    # raise an error if nothing has been found
    if finalName is None:
        raise NameTranslationError("No unique name could be found.")
    # finished
    return finalName

