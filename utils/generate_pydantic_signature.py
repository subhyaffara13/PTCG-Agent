from typing import Callable

def generate_pydantic_signature(
    init: Callable[..., None],
    fields: dict[str, FieldInfo],
    validate_by_name: bool,
    extra: ExtraValues | None,
    is_dataclass: bool = False,
) -> Signature:
    """Generate signature for a pydantic BaseModel or dataclass.

    Args:
        init: The class init.
        fields: The model fields.
        validate_by_name: The `validate_by_name` value of the config.
        extra: The `extra` value of the config.
        is_dataclass: Whether the model is a dataclass.

    Returns:
        The dataclass/BaseModel subclass signature.
    """
    merged_params = _generate_signature_parameters(init, fields, validate_by_name, extra)

    if is_dataclass:
        merged_params = {k: _process_param_defaults(v) for k, v in merged_params.items()}

    return Signature(parameters=list(merged_params.values()), return_annotation=None)

