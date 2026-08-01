
def _ngettext(message: str, plural: str, num: int) -> str:
    """Plural version of _gettext.

    Args:
        message (str): Singular text to translate.
        plural (str): Plural text to translate.
        num (int): The number (e.g. item count) to determine translation for the
            respective grammatical number.

    Returns:
        str: Translated text.
    """
    return get_translation().ngettext(message, plural, num)

