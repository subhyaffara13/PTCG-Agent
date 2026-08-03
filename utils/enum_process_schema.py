from typing import Any, Dict, Optional

def enum_process_schema(enum: Type[Enum], *, field: Optional[ModelField] = None) -> Dict[str, Any]:
    """
    Take a single `enum` and generate its schema.

    This is similar to the `model_process_schema` function, but applies to ``Enum`` objects.
    """
    import inspect

    schema_: Dict[str, Any] = {
        'title': enum.__name__,
        # Python assigns all enums a default docstring value of 'An enumeration', so
        # all enums will have a description field even if not explicitly provided.
        'description': inspect.cleandoc(enum.__doc__ or 'An enumeration.'),
        # Add enum values and the enum field type to the schema.
        'enum': [item.value for item in cast(Iterable[Enum], enum)],
    }

    add_field_type_to_schema(enum, schema_)

    modify_schema = getattr(enum, '__modify_schema__', None)
    if modify_schema:
        _apply_modify_schema(modify_schema, field, schema_)

    return schema_

