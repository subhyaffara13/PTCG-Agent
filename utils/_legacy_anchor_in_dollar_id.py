
def _legacy_anchor_in_dollar_id(
    specification: Specification[Schema],
    contents: Schema,
) -> Iterable[Anchor[Schema]]:
    if isinstance(contents, bool):
        return []
    id = contents.get("$id", "")
    if not id.startswith("#"):
        return []
    return [
        Anchor(
            name=id[1:],
            resource=specification.create_resource(contents),
        ),
    ]

