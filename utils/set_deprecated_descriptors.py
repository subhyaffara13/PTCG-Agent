
def set_deprecated_descriptors(cls: type[BaseModel]) -> None:
    """Set data descriptors on the class for deprecated fields."""
    for field, field_info in cls.__pydantic_fields__.items():
        if (msg := field_info.deprecation_message) is not None:
            desc = _DeprecatedFieldDescriptor(msg)
            desc.__set_name__(cls, field)
            setattr(cls, field, desc)

    for field, computed_field_info in cls.__pydantic_computed_fields__.items():
        if (
            (msg := computed_field_info.deprecation_message) is not None
            # Avoid having two warnings emitted:
            and not hasattr(unwrap_wrapped_function(computed_field_info.wrapped_property), '__deprecated__')
        ):
            desc = _DeprecatedFieldDescriptor(msg, computed_field_info.wrapped_property)
            desc.__set_name__(cls, field)
            setattr(cls, field, desc)

