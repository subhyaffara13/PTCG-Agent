
def check_nfc(label: str) -> None:
    """Require that a label is in Unicode Normalization Form C.

    :param label: The label to check.
    :raises IDNAError: If ``label`` differs from its NFC normalisation.
    """
    if len(label) > _max_input_length:
        raise IDNAError("Label too long")
    if unicodedata.normalize("NFC", label) != label:
        raise IDNAError("Label must be in Normalization Form C")


def check_nfc(label: str) -> None:
    if unicodedata.normalize("NFC", label) != label:
        raise IDNAError("Label must be in Normalization Form C")

