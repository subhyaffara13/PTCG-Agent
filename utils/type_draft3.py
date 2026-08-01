
def type_draft3(validator, types, instance, schema):
    types = _utils.ensure_list(types)

    all_errors = []
    for index, type in enumerate(types):
        if validator.is_type(type, "object"):
            errors = list(validator.descend(instance, type, schema_path=index))
            if not errors:
                return
            all_errors.extend(errors)
        elif validator.is_type(instance, type):
                return

    reprs = []
    for type in types:
        try:
            reprs.append(repr(type["name"]))
        except Exception:  # noqa: BLE001
            reprs.append(repr(type))
    yield ValidationError(
        f"{instance!r} is not of type {', '.join(reprs)}",
        context=all_errors,
    )

