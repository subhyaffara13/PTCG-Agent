
def alabel(label: str) -> bytes:
    """Convert a single U-label into its A-label form.

    The result is the ASCII-Compatible Encoding (ACE) form per :rfc:`5891`
    §4: the label is validated, Punycode-encoded, and prefixed with
    ``xn--``. Pure ASCII labels that are already valid IDNA labels are
    returned unchanged (as :class:`bytes`).

    :param label: The label to convert, as a Unicode string.
    :returns: The A-label as ASCII-encoded :class:`bytes`.
    :raises IDNAError: If the label is invalid or the resulting A-label
        exceeds 63 octets.
    """
    if len(label) > _max_input_length:
        raise IDNAError("Label too long")
    try:
        label_bytes = label.encode("ascii")
    except UnicodeEncodeError:
        pass
    else:
        ulabel(label_bytes)
        if not valid_label_length(label_bytes):
            raise IDNAError("Label too long")
        return label_bytes

    check_label(label)
    label_bytes = _alabel_prefix + _punycode(label)

    if not valid_label_length(label_bytes):
        raise IDNAError("Label too long")

    return label_bytes


def alabel(label: str) -> bytes:
    try:
        label_bytes = label.encode("ascii")
        ulabel(label_bytes)
        if not valid_label_length(label_bytes):
            raise IDNAError("Label too long")
        return label_bytes
    except UnicodeEncodeError:
        pass

    check_label(label)
    label_bytes = _alabel_prefix + _punycode(label)

    if not valid_label_length(label_bytes):
        raise IDNAError("Label too long")

    return label_bytes

