
def _extract_fields_recursive(
    model: Type[BaseModel],
    depth: int = 0,
) -> Dict[str, Any]:
    # Check if we've exceeded the maximum recursion depth
    if depth > DEFAULT_MAX_RECURSE_DEPTH:
        raise HTTPException(
            status_code=400,
            detail=f"Max depth of {DEFAULT_MAX_RECURSE_DEPTH} exceeded while processing model fields. Please check the model structure for excessive nesting.",
        )

    fields = {}

    for field_name, field in model.model_fields.items():
        field_annotation = field.annotation

        # Skip optional_params if it's not meaningfully overridden
        if _should_skip_optional_params(
            field_name=field_name, field_annotation=field_annotation
        ):
            continue

        # Handle Optional types and get the actual type
        if field_annotation is None:
            continue

        field_annotation = _unwrap_optional_type(field_annotation=field_annotation)

        # Get field metadata
        description = field.description or field_name
        required = field.is_required()

        # Check if this is a BaseModel subclass
        is_basemodel_subclass = (
            inspect.isclass(field_annotation)
            and issubclass(field_annotation, BaseModel)
            and field_annotation is not BaseModel
        )

        if is_basemodel_subclass:
            # Recursively get fields from the nested model
            nested_fields = _extract_fields_recursive(
                cast(Type[BaseModel], field_annotation), depth + 1
            )
            fields[field_name] = {
                "description": description,
                "required": required,
                "type": "nested",
                "fields": nested_fields,
            }
        else:
            fields[field_name] = _build_field_dict(
                field=field,
                field_annotation=field_annotation,
                description=description,
                required=required,
            )

    return fields

