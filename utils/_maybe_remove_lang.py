
def _maybe_remove_lang(text: str, skip_special_tokens: bool) -> str: ...


def _maybe_remove_lang(text: list[str], skip_special_tokens: bool) -> list[str]: ...


def _maybe_remove_lang(text: str | list[str], skip_special_tokens: bool) -> str | list[str]:
    # in the specific case of Voxtral, the added f"lang:xx" (always a two char language code since it follows ISO 639-1 alpha-2 format)
    # is not considered as a special token by mistral-common and is encoded/ decoded as normal text.
    # Nevertheless we should remove it to ease users life.
    if not skip_special_tokens:
        return text

    if isinstance(text, str):
        return re.sub(r"^lang:[a-z]{2}", "", text)

    return [re.sub(r"^lang:[a-z]{2}", "", string) for string in text]

