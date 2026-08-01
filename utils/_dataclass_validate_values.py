
def _dataclass_validate_values(self: 'Dataclass') -> None:
    # validation errors can occur if this function is called twice on an already initialised dataclass.
    # for example if Extra.forbid is enabled, it would consider __pydantic_initialised__ an invalid extra property
    if getattr(self, '__pydantic_initialised__'):
        return
    if getattr(self, '__pydantic_has_field_info_default__', False):
        # We need to remove `FieldInfo` values since they are not valid as input
        # It's ok to do that because they are obviously the default values!
        input_data = {
            k: v
            for k, v in self.__dict__.items()
            if not (isinstance(v, FieldInfo) or _is_field_cached_property(self, k))
        }
    else:
        input_data = {k: v for k, v in self.__dict__.items() if not _is_field_cached_property(self, k)}
    d, _, validation_error = validate_model(self.__pydantic_model__, input_data, cls=self.__class__)
    if validation_error:
        raise validation_error
    self.__dict__.update(d)
    object.__setattr__(self, '__pydantic_initialised__', True)

