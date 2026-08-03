from typing import Any

def rebuild_dataclass_fields(
    cls: type[PydanticDataclass],
    *,
    config_wrapper: ConfigWrapper,
    ns_resolver: NsResolver,
    typevars_map: Mapping[TypeVar, Any],
) -> dict[str, FieldInfo]:
    """Rebuild the (already present) dataclass fields by trying to reevaluate annotations.

    This function should be called whenever a dataclass with incomplete fields is encountered.

    Raises:
        NameError: If one of the annotations failed to evaluate.

    Note:
        This function *doesn't* mutate the dataclass fields in place, as it can be called during
        schema generation, where you don't want to mutate other dataclass's fields.
    """
    FieldInfo_ = import_cached_field_info()

    rebuilt_fields: dict[str, FieldInfo] = {}
    with ns_resolver.push(cls):
        for f_name, field_info in cls.__pydantic_fields__.items():
            if field_info._complete:
                rebuilt_fields[f_name] = field_info
            else:
                existing_desc = field_info.description
                ann = _typing_extra.eval_type(
                    field_info._original_annotation,
                    *ns_resolver.types_namespace,
                )
                ann = _generics.replace_types(ann, typevars_map)
                new_field = FieldInfo_.from_annotated_attribute(
                    ann,
                    field_info._original_assignment,
                    _source=AnnotationSource.DATACLASS,
                )

                # The description might come from the docstring if `use_attribute_docstrings` was `True`:
                new_field.description = new_field.description if new_field.description is not None else existing_desc
                update_field_from_config(config_wrapper, f_name, new_field)
                rebuilt_fields[f_name] = new_field

    return rebuilt_fields

