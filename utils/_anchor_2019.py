
def _anchor_2019(
    specification: Specification[Schema],
    contents: Schema,
) -> Iterable[Anchor[Schema]]:
    if isinstance(contents, bool):
        return []
    anchor = contents.get("$anchor")
    if anchor is None:
        return []
    return [
        Anchor(
            name=anchor,
            resource=specification.create_resource(contents),
        ),
    ]

