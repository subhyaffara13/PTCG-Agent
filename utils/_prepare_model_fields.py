
def _prepare_model_fields(
    created_model: Type[GenericModel],
    fields: Mapping[str, Any],
    instance_type_hints: Mapping[str, type],
    typevars_map: Mapping[Any, type],
) -> None:
    """
    Replace DeferredType fields with concrete type hints and prepare them.
    """

    for key, field in created_model.__fields__.items():
        if key not in fields:
            assert field.type_.__class__ is not DeferredType
            # https://github.com/nedbat/coveragepy/issues/198
            continue  # pragma: no cover

        assert field.type_.__class__ is DeferredType, field.type_.__class__

        field_type_hint = instance_type_hints[key]
        concrete_type = replace_types(field_type_hint, typevars_map)
        field.type_ = concrete_type
        field.outer_type_ = concrete_type
        field.prepare()
        created_model.__annotations__[key] = concrete_type

