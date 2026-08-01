
def parse_obj_as(type_: type[T], obj: Any, type_name: NameFactory | None = None) -> T:
    warnings.warn(
        '`parse_obj_as` is deprecated. Use `pydantic.TypeAdapter.validate_python` instead.',
        category=PydanticDeprecatedSince20,
        stacklevel=2,
    )
    if type_name is not None:  # pragma: no cover
        warnings.warn(
            'The type_name parameter is deprecated. parse_obj_as no longer creates temporary models',
            DeprecationWarning,
            stacklevel=2,
        )
    return TypeAdapter(type_).validate_python(obj)


def parse_obj_as(type_: Type[T], obj: Any, *, type_name: Optional[NameFactory] = None) -> T:
    model_type = _get_parsing_type(type_, type_name=type_name)  # type: ignore[arg-type]
    return model_type(__root__=obj).__root__

