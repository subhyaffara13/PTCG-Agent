
def _process_param_defaults(param: Parameter) -> Parameter:
    """Modify the signature for a parameter in a dataclass where the default value is a FieldInfo instance.

    Args:
        param (Parameter): The parameter

    Returns:
        Parameter: The custom processed parameter
    """
    from ..fields import FieldInfo

    param_default = param.default
    if isinstance(param_default, FieldInfo):
        annotation = param.annotation
        # Replace the annotation if appropriate
        # inspect does "clever" things to show annotations as strings because we have
        # `from __future__ import annotations` in main, we don't want that
        if annotation == 'Any':
            annotation = Any

        # Replace the field default
        default = param_default.default
        if default is PydanticUndefined:
            if param_default.default_factory is None:
                default = Signature.empty
            else:
                # this is used by dataclasses to indicate a factory exists:
                default = dataclasses._HAS_DEFAULT_FACTORY  # type: ignore
        return param.replace(
            annotation=annotation, name=_field_name_for_signature(param.name, param_default), default=default
        )
    return param

