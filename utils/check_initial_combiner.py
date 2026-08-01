
def check_initial_combiner(label: str) -> bool:
    """Reject labels that begin with a combining mark.

    Per :rfc:`5891` §4.2.3.2 a label must not start with a character of
    Unicode general category ``M`` (Mark).

    :param label: The label to check.
    :returns: ``True`` if the first character is not a combining mark.
    :raises IDNAError: If the label begins with a combining character.
    """
    if unicodedata.category(label[0])[0] == "M":
        raise IDNAError("Label begins with an illegal combining character")
    return True


def check_initial_combiner(label: str) -> bool:
    if unicodedata.category(label[0])[0] == "M":
        raise IDNAError("Label begins with an illegal combining character")
    return True

