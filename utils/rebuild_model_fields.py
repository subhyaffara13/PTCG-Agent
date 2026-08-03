from typing import Any

def rebuild_model_fields(
    cls: type[BaseModel],
    *,
    config_wrapper: ConfigWrapper,
    ns_resolver: NsResolver,
    typevars_map: Mapping[TypeVar, Any],
) -> tuple[dict[str, FieldInfo], PydanticExtraInfo | None]:
    """Rebuild the (already present) model fields by trying to reevaluate annotations.

    This function should be called whenever a model with incomplete fields is encountered.

    Returns:
        A two-tuple, the first element being the rebuilt fields, the second element being
        the rebuild `PydanticExtraInfo` instance, if available.

    Raises:
        NameError: If one of the annotations failed to evaluate.

    Note:
        This function *doesn't* mutate the model fields in place, as it can be called during
        schema generation, where you don't want to mutate other model's fields.
    """
    rebuilt_fields: dict[str, FieldInfo] = {}
    with ns_resolver.push(cls):
        for f_name, field_info in cls.__pydantic_fields__.items():
            if field_info._complete:
                rebuilt_fields[f_name] = field_info
            else:
                new_field = _recreate_field_info(
                    field_info, ns_resolver=ns_resolver, typevars_map=typevars_map, lenient=False
                )
                update_field_from_config(config_wrapper, f_name, new_field)
                rebuilt_fields[f_name] = new_field

        if cls.__pydantic_extra_info__ is not None and not cls.__pydantic_extra_info__.complete:
            rebuilt_extra_info = PydanticExtraInfo(
                annotation=_typing_extra.eval_type(
                    cls.__pydantic_extra_info__.annotation, *ns_resolver.types_namespace
                ),
                complete=True,
            )
        else:
            rebuilt_extra_info = cls.__pydantic_extra_info__

    return rebuilt_fields, rebuilt_extra_info

