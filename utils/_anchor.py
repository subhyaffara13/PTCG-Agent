
def _anchor(
    specification: Specification[Schema],
    contents: Schema,
) -> Iterable[AnchorType[Schema]]:
    if isinstance(contents, bool):
        return
    anchor = contents.get("$anchor")
    if anchor is not None:
        yield Anchor(
            name=anchor,
            resource=specification.create_resource(contents),
        )

    dynamic_anchor = contents.get("$dynamicAnchor")
    if dynamic_anchor is not None:
        yield DynamicAnchor(
            name=dynamic_anchor,
            resource=specification.create_resource(contents),
        )

