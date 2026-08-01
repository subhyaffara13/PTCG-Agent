
def valid_contextj(label: str, pos: int) -> bool:
    """Validate the CONTEXTJ rules from :rfc:`5892` Appendix A.

    These rules govern the contextual use of the joiner codepoints
    ``U+200C`` (ZERO WIDTH NON-JOINER, Appendix A.1) and ``U+200D``
    (ZERO WIDTH JOINER, Appendix A.2) within a label.

    :param label: The label containing the codepoint.
    :param pos: Index of the joiner codepoint within ``label``.
    :returns: ``True`` if the codepoint at ``pos`` satisfies its CONTEXTJ
        rule, ``False`` otherwise (including when the codepoint at
        ``pos`` is not a recognised joiner).
    :raises ValueError: If an adjacent codepoint has no Unicode name when
        determining its combining class.
    :raises IDNAError: If ``label`` exceeds the defensive input length limit.
    """
    if len(label) > _max_input_length:
        raise IDNAError("Label too long")
    cp_value = ord(label[pos])

    if cp_value == 0x200C:
        if pos > 0 and _combining_class(ord(label[pos - 1])) == _virama_combining_class:
            return True

        ok = False
        for i in range(pos - 1, -1, -1):
            joining_type = _joining_type(ord(label[i]))
            if joining_type == "T":
                continue
            if joining_type in _bidi_joiner_l_or_d:
                ok = True
                break
            break

        if not ok:
            return False

        ok = False
        for i in range(pos + 1, len(label)):
            joining_type = _joining_type(ord(label[i]))
            if joining_type == "T":
                continue
            if joining_type in _bidi_joiner_r_or_d:
                ok = True
                break
            break
        return ok

    if cp_value == 0x200D:
        return pos > 0 and _combining_class(ord(label[pos - 1])) == _virama_combining_class

    return False


def valid_contextj(label: str, pos: int) -> bool:
    cp_value = ord(label[pos])

    if cp_value == 0x200C:
        if pos > 0:
            if _combining_class(ord(label[pos - 1])) == _virama_combining_class:
                return True

        ok = False
        for i in range(pos - 1, -1, -1):
            joining_type = idnadata.joining_types.get(ord(label[i]))
            if joining_type == ord("T"):
                continue
            elif joining_type in [ord("L"), ord("D")]:
                ok = True
                break
            else:
                break

        if not ok:
            return False

        ok = False
        for i in range(pos + 1, len(label)):
            joining_type = idnadata.joining_types.get(ord(label[i]))
            if joining_type == ord("T"):
                continue
            elif joining_type in [ord("R"), ord("D")]:
                ok = True
                break
            else:
                break
        return ok

    if cp_value == 0x200D:
        if pos > 0:
            if _combining_class(ord(label[pos - 1])) == _virama_combining_class:
                return True
        return False

    else:
        return False

