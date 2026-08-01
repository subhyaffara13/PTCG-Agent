
def items(validator, items, instance, schema):
    if not validator.is_type(instance, "array"):
        return

    prefix = len(schema.get("prefixItems", []))
    total = len(instance)
    extra = total - prefix
    if extra <= 0:
        return

    if items is False:
        rest = instance[prefix:] if extra != 1 else instance[prefix]
        item = "items" if prefix != 1 else "item"
        yield ValidationError(
            f"Expected at most {prefix} {item} but found {extra} "
            f"extra: {rest!r}",
        )
    else:
        for index in range(prefix, total):
            yield from validator.descend(
                instance=instance[index],
                schema=items,
                path=index,
            )

