from typing import Union

def check_label(label: Union[str, bytes, bytearray]) -> None:
    """Run the full set of IDNA 2008 validity checks on a single label.

    Applies, in order: NFC normalisation (:func:`check_nfc`), hyphen
    restrictions (:func:`check_hyphen_ok`), the no-leading-combiner rule
    (:func:`check_initial_combiner`), per-codepoint validity (PVALID,
    CONTEXTJ, CONTEXTO classes from :rfc:`5892`), and the Bidi Rule
    (:func:`check_bidi`).

    :param label: The label to validate. ``bytes`` or ``bytearray`` input
        is decoded as UTF-8 first.
    :raises IDNAError: If the label is empty or fails a structural rule.
    :raises InvalidCodepoint: If the label contains a DISALLOWED or
        UNASSIGNED codepoint.
    :raises InvalidCodepointContext: If a CONTEXTJ or CONTEXTO codepoint
        is not valid in its context.
    :raises IDNABidiError: If the Bidi Rule is violated.
    """
    if len(label) > _max_input_length:
        raise IDNAError("Label too long")
    if isinstance(label, (bytes, bytearray)):
        label = label.decode("utf-8")
    if len(label) == 0:
        raise IDNAError("Empty Label")

    # Reject on domain length rather than label length so support some UTS 46
    # use cases, still reducing processing of label contextual rules
    if not valid_string_length(label, trailing_dot=True):
        raise IDNAError("Label too long")

    check_nfc(label)
    check_hyphen_ok(label)
    check_initial_combiner(label)

    for pos, cp in enumerate(label):
        cp_value = ord(cp)
        if intranges_contain(cp_value, idnadata.codepoint_classes["PVALID"]):
            continue
        if intranges_contain(cp_value, idnadata.codepoint_classes["CONTEXTJ"]):
            try:
                if not valid_contextj(label, pos):
                    raise InvalidCodepointContext(f"Joiner {_unot(cp_value)} not allowed at position {pos + 1} in {label!r}")
            except ValueError as err:
                raise IDNAError(
                    f"Unknown codepoint adjacent to joiner {_unot(cp_value)} at position {pos + 1} in {label!r}"
                ) from err
        elif intranges_contain(cp_value, idnadata.codepoint_classes["CONTEXTO"]):
            if not valid_contexto(label, pos):
                raise InvalidCodepointContext(f"Codepoint {_unot(cp_value)} not allowed at position {pos + 1} in {label!r}")
        else:
            raise InvalidCodepoint(f"Codepoint {_unot(cp_value)} at position {pos + 1} of {label!r} not allowed")

    check_bidi(label)


def check_label(label: Union[str, bytes, bytearray]) -> None:
    if isinstance(label, (bytes, bytearray)):
        label = label.decode("utf-8")
    if len(label) == 0:
        raise IDNAError("Empty Label")

    check_nfc(label)
    check_hyphen_ok(label)
    check_initial_combiner(label)

    for pos, cp in enumerate(label):
        cp_value = ord(cp)
        if intranges_contain(cp_value, idnadata.codepoint_classes["PVALID"]):
            continue
        elif intranges_contain(cp_value, idnadata.codepoint_classes["CONTEXTJ"]):
            try:
                if not valid_contextj(label, pos):
                    raise InvalidCodepointContext(
                        "Joiner {} not allowed at position {} in {}".format(_unot(cp_value), pos + 1, repr(label))
                    )
            except ValueError:
                raise IDNAError(
                    "Unknown codepoint adjacent to joiner {} at position {} in {}".format(
                        _unot(cp_value), pos + 1, repr(label)
                    )
                )
        elif intranges_contain(cp_value, idnadata.codepoint_classes["CONTEXTO"]):
            if not valid_contexto(label, pos):
                raise InvalidCodepointContext(
                    "Codepoint {} not allowed at position {} in {}".format(_unot(cp_value), pos + 1, repr(label))
                )
        else:
            raise InvalidCodepoint(
                "Codepoint {} at position {} of {} not allowed".format(_unot(cp_value), pos + 1, repr(label))
            )

    check_bidi(label)

