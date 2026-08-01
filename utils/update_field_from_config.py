
def update_field_from_config(config_wrapper: ConfigWrapper, field_name: str, field_info: FieldInfo) -> None:
    """Update the `FieldInfo` instance from the configuration set on the model it belongs to.

    This will apply the title and alias generators from the configuration.

    Args:
        config_wrapper: The configuration from the model.
        field_name: The field name the `FieldInfo` instance is attached to.
        field_info: The `FieldInfo` instance to update.
    """
    field_title_generator = field_info.field_title_generator or config_wrapper.field_title_generator
    if field_title_generator is not None:
        _apply_field_title_generator_to_field_info(field_title_generator, field_name, field_info)
    if config_wrapper.alias_generator is not None:
        _apply_alias_generator_to_field_info(config_wrapper.alias_generator, field_name, field_info)

