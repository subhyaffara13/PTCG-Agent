
def model_dump_with_preserved_fields(
    obj: Any,
    preserve_fields: Optional[List[str]] = None,
    exclude_unset: bool = True,
) -> Dict[str, Any]:
    """
    Serialize a Pydantic model to a dictionary while preserving specific fields
    even if they are None.

    Fields listed in _PRESERVED_NONE_FIELDS are restored after
    model_dump(exclude_none=True) strips them.

    Args:
        obj: The Pydantic BaseModel instance to serialize
        preserve_fields: Deprecated, kept for backward compatibility.
        exclude_unset: Whether to exclude fields that were not explicitly set

    Returns:
        Dictionary representation with None values excluded except for preserved fields
    """
    result = obj.model_dump(exclude_none=True, exclude_unset=exclude_unset)

    choices = result.get("choices")
    if not choices:
        return result

    obj_choices = obj.choices
    for choice_obj, choice_dict in zip(obj_choices, choices):
        for sub_object, field_name in _PRESERVED_NONE_FIELDS:
            sub_dict = choice_dict.get(sub_object)
            if sub_dict is None:
                continue
            if field_name not in sub_dict:
                sub_obj = getattr(choice_obj, sub_object, None)
                if sub_obj is not None and hasattr(sub_obj, field_name):
                    sub_dict[field_name] = getattr(sub_obj, field_name)

    return result

