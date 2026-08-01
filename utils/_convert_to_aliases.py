
def _convert_to_aliases(
    alias: str | AliasChoices | AliasPath | None,
) -> str | list[str | int] | list[list[str | int]] | None:
    if isinstance(alias, (AliasChoices, AliasPath)):
        return alias.convert_to_aliases()
    else:
        return alias

