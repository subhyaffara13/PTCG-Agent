
def valid_contexto(label: str, pos: int, exception: bool = False) -> bool:
    """Validate the CONTEXTO rules from :rfc:`5892` Appendix A.

    Covers the contextual rules for codepoints such as MIDDLE DOT
    (``U+00B7``), Greek lower numeral sign, Hebrew punctuation, Katakana
    middle dot, and the Arabic-Indic / Extended Arabic-Indic digit ranges.

    :param label: The label containing the codepoint.
    :param pos: Index of the codepoint within ``label``.
    :param exception: Reserved for forward compatibility; currently unused.
    :returns: ``True`` if the codepoint at ``pos`` satisfies its CONTEXTO
        rule, ``False`` otherwise (including when the codepoint is not a
        recognised CONTEXTO codepoint).
    :raises IDNAError: If ``label`` exceeds the defensive input length limit.
    """
    if len(label) > _max_input_length:
        raise IDNAError("Label too long")
    cp_value = ord(label[pos])

    if cp_value == 0x00B7:
        return 0 < pos < len(label) - 1 and ord(label[pos - 1]) == 0x006C and ord(label[pos + 1]) == 0x006C

    if cp_value == 0x0375:
        if pos < len(label) - 1 and len(label) > 1:
            return _is_script(label[pos + 1], "Greek")
        return False

    if cp_value in {0x05F3, 0x05F4}:
        if pos > 0:
            return _is_script(label[pos - 1], "Hebrew")
        return False

    if cp_value == 0x30FB:
        for cp in label:
            if cp == "\u30fb":
                continue
            if _is_script(cp, "Hiragana") or _is_script(cp, "Katakana") or _is_script(cp, "Han"):
                return True
        return False

    if 0x660 <= cp_value <= 0x669:
        return not any(0x6F0 <= ord(cp) <= 0x06F9 for cp in label)

    if 0x6F0 <= cp_value <= 0x6F9:
        return not any(0x660 <= ord(cp) <= 0x0669 for cp in label)

    return False


def valid_contexto(label: str, pos: int, exception: bool = False) -> bool:
    cp_value = ord(label[pos])

    if cp_value == 0x00B7:
        if 0 < pos < len(label) - 1:
            if ord(label[pos - 1]) == 0x006C and ord(label[pos + 1]) == 0x006C:
                return True
        return False

    elif cp_value == 0x0375:
        if pos < len(label) - 1 and len(label) > 1:
            return _is_script(label[pos + 1], "Greek")
        return False

    elif cp_value == 0x05F3 or cp_value == 0x05F4:
        if pos > 0:
            return _is_script(label[pos - 1], "Hebrew")
        return False

    elif cp_value == 0x30FB:
        for cp in label:
            if cp == "\u30fb":
                continue
            if _is_script(cp, "Hiragana") or _is_script(cp, "Katakana") or _is_script(cp, "Han"):
                return True
        return False

    elif 0x660 <= cp_value <= 0x669:
        for cp in label:
            if 0x6F0 <= ord(cp) <= 0x06F9:
                return False
        return True

    elif 0x6F0 <= cp_value <= 0x6F9:
        for cp in label:
            if 0x660 <= ord(cp) <= 0x0669:
                return False
        return True

    return False

