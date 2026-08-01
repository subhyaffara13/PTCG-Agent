
def validate_custom_root_type(fields: Dict[str, ModelField]) -> None:
    if len(fields) > 1:
        raise ValueError(f'{ROOT_KEY} cannot be mixed with other fields')

