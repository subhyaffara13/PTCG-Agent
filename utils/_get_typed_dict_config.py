
def _get_typed_dict_config(cls: type[Any] | None) -> ConfigDict:
    if cls is not None:
        try:
            return _decorators.get_attribute_from_bases(cls, '__pydantic_config__')
        except AttributeError:
            pass
    return {}

