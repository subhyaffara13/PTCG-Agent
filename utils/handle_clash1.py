
def handleClash1(userName, existing=[], prefix="", suffix=""):
    """
    existing should be a case-insensitive list
    of all existing file names.

    >>> prefix = ("0" * 5) + "."
    >>> suffix = "." + ("0" * 10)
    >>> existing = ["a" * 5]

    >>> e = list(existing)
    >>> handleClash1(userName="A" * 5, existing=e,
    ...		prefix=prefix, suffix=suffix) == (
    ... 	'00000.AAAAA000000000000001.0000000000')
    True

    >>> e = list(existing)
    >>> e.append(prefix + "aaaaa" + "1".zfill(15) + suffix)
    >>> handleClash1(userName="A" * 5, existing=e,
    ...		prefix=prefix, suffix=suffix) == (
    ... 	'00000.AAAAA000000000000002.0000000000')
    True

    >>> e = list(existing)
    >>> e.append(prefix + "AAAAA" + "2".zfill(15) + suffix)
    >>> handleClash1(userName="A" * 5, existing=e,
    ...		prefix=prefix, suffix=suffix) == (
    ... 	'00000.AAAAA000000000000001.0000000000')
    True
    """
    # if the prefix length + user name length + suffix length + 15 is at
    # or past the maximum length, silce 15 characters off of the user name
    prefixLength = len(prefix)
    suffixLength = len(suffix)
    if prefixLength + len(userName) + suffixLength + 15 > maxFileNameLength:
        l = prefixLength + len(userName) + suffixLength + 15
        sliceLength = maxFileNameLength - l
        userName = userName[:sliceLength]
    finalName = None
    # try to add numbers to create a unique name
    counter = 1
    while finalName is None:
        name = userName + str(counter).zfill(15)
        fullName = prefix + name + suffix
        if fullName.lower() not in existing:
            finalName = fullName
            break
        else:
            counter += 1
        if counter >= 999999999999999:
            break
    # if there is a clash, go to the next fallback
    if finalName is None:
        finalName = handleClash2(existing, prefix, suffix)
    # finished
    return finalName


def handleClash1(
    userName: str, existing: Iterable[str] = [], prefix: str = "", suffix: str = ""
) -> str:
    """A helper function that resolves collisions with existing names when choosing a filename.

    This function attempts to append an unused integer counter to the filename.

        Args:
                userName (str): The input file name.
                existing: A case-insensitive list of all existing file names.
                prefix: Prefix to be prepended to the file name.
                suffix: Suffix to be appended to the file name.

        Returns:
                A suitable filename.

        >>> prefix = ("0" * 5) + "."
        >>> suffix = "." + ("0" * 10)
        >>> existing = ["a" * 5]

        >>> e = list(existing)
        >>> handleClash1(userName="A" * 5, existing=e,
        ...		prefix=prefix, suffix=suffix) == (
        ... 	'00000.AAAAA000000000000001.0000000000')
        True

        >>> e = list(existing)
        >>> e.append(prefix + "aaaaa" + "1".zfill(15) + suffix)
        >>> handleClash1(userName="A" * 5, existing=e,
        ...		prefix=prefix, suffix=suffix) == (
        ... 	'00000.AAAAA000000000000002.0000000000')
        True

        >>> e = list(existing)
        >>> e.append(prefix + "AAAAA" + "2".zfill(15) + suffix)
        >>> handleClash1(userName="A" * 5, existing=e,
        ...		prefix=prefix, suffix=suffix) == (
        ... 	'00000.AAAAA000000000000001.0000000000')
        True
    """
    # if the prefix length + user name length + suffix length + 15 is at
    # or past the maximum length, silce 15 characters off of the user name
    prefixLength = len(prefix)
    suffixLength = len(suffix)
    if prefixLength + len(userName) + suffixLength + 15 > maxFileNameLength:
        l = prefixLength + len(userName) + suffixLength + 15
        sliceLength = maxFileNameLength - l
        userName = userName[:sliceLength]
    finalName = None
    # try to add numbers to create a unique name
    counter = 1
    while finalName is None:
        name = userName + str(counter).zfill(15)
        fullName = prefix + name + suffix
        if fullName.lower() not in existing:
            finalName = fullName
            break
        else:
            counter += 1
        if counter >= 999999999999999:
            break
    # if there is a clash, go to the next fallback
    if finalName is None:
        finalName = handleClash2(existing, prefix, suffix)
    # finished
    return finalName

