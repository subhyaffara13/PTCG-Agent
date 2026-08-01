
def _apply_field_title_generator_to_field_info(
    title_generator: Callable[[str, FieldInfo], str],
    field_name: str,
    field_info: FieldInfo,
):
    if field_info.title is None:
        title = title_generator(field_name, field_info)
        if not isinstance(title, str):
            raise TypeError(f'field_title_generator {title_generator} must return str, not {title.__class__}')

        field_info.title = title

