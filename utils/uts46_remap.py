
def uts46_remap(domain: str, std3_rules: bool = True, transitional: bool = False) -> str:
    """Apply the UTS #46 character mapping to a domain string.

    Implements the mapping table from `UTS #46 §4
    <https://www.unicode.org/reports/tr46/>`_: each character is kept,
    replaced, or rejected based on its status (``V``, ``M``, ``D``, ``3``,
    ``I``). The result is returned in Normalisation Form C.

    :param domain: The full domain name to remap.
    :param std3_rules: If ``True``, apply the stricter STD3 ASCII rules
        (status ``3`` codepoints raise instead of being kept or mapped).
    :param transitional: If ``True``, use transitional processing (status
        ``D`` codepoints are mapped instead of kept). Transitional
        processing has been removed from UTS #46 and this option is
        retained only for backwards compatibility.
    :returns: The remapped domain, in Normalisation Form C.
    :raises InvalidCodepoint: If the domain contains a disallowed
        codepoint under the chosen rules.
    :raises IDNAError: If ``domain`` exceeds the defensive input length limit.
    """
    if len(domain) > _max_input_length:
        raise IDNAError("Domain too long")
    from .uts46data import uts46_replacements, uts46_starts, uts46_statuses

    output = ""

    for pos, char in enumerate(domain):
        code_point = ord(char)
        i = code_point if code_point < 256 else bisect.bisect_right(uts46_starts, code_point) - 1
        status = chr(uts46_statuses[i])
        replacement: Optional[str] = uts46_replacements[i]

        # UTS #46 §4: V is always valid, D is deviation (kept unless transitional),
        # 3 is disallowed-STD3 (kept unmapped if std3_rules is off and no mapping).
        keep_as_is = (
            status == "V" or (status == "D" and not transitional) or (status == "3" and not std3_rules and replacement is None)
        )
        # M is mapped, 3-with-replacement and transitional D fall through to the
        # same replacement output path.
        use_replacement = replacement is not None and (
            status == "M" or (status == "3" and not std3_rules) or (status == "D" and transitional)
        )

        if keep_as_is:
            output += char
        elif use_replacement:
            assert replacement is not None  # narrowed by use_replacement
            output += replacement
        elif status == "I":
            continue
        else:
            raise InvalidCodepoint(f"Codepoint {_unot(code_point)} not allowed at position {pos + 1} in {domain!r}")

    return unicodedata.normalize("NFC", output)


def uts46_remap(domain: str, std3_rules: bool = True, transitional: bool = False) -> str:
    """Re-map the characters in the string according to UTS46 processing."""
    from .uts46data import uts46data

    output = ""

    for pos, char in enumerate(domain):
        code_point = ord(char)
        try:
            uts46row = uts46data[code_point if code_point < 256 else bisect.bisect_left(uts46data, (code_point, "Z")) - 1]
            status = uts46row[1]
            replacement: Optional[str] = None
            if len(uts46row) == 3:
                replacement = uts46row[2]
            if (
                status == "V"
                or (status == "D" and not transitional)
                or (status == "3" and not std3_rules and replacement is None)
            ):
                output += char
            elif replacement is not None and (
                status == "M" or (status == "3" and not std3_rules) or (status == "D" and transitional)
            ):
                output += replacement
            elif status != "I":
                raise IndexError()
        except IndexError:
            raise InvalidCodepoint(
                "Codepoint {} not allowed at position {} in {}".format(_unot(code_point), pos + 1, repr(domain))
            )

    return unicodedata.normalize("NFC", output)

