
def _reject_duplicate_attribute(
    oid: ObjectIdentifier,
    attributes: list[tuple[ObjectIdentifier, bytes, int | None]],
) -> None:
    # This is quadratic in the number of attributes
    for attr_oid, _, _ in attributes:
        if attr_oid == oid:
            raise ValueError("This attribute has already been set.")

