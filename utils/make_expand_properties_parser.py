
def make_expand_properties_parser(valid_properties: Sequence[ExpandPropertyT]):
    """Create a callback to parse and validate comma-separated expand properties."""

    def _parse_expand_properties(value: str | None) -> list[ExpandPropertyT] | None:
        if value is None:
            return None
        properties = [p.strip() for p in value.split(",")]
        for prop in properties:
            if prop not in valid_properties:
                raise typer.BadParameter(
                    f"Invalid expand property: '{prop}'. Valid values are: {', '.join(valid_properties)}"
                )
        return [cast(ExpandPropertyT, prop) for prop in properties]

    return _parse_expand_properties

