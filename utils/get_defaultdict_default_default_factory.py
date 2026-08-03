from typing import Any, Callable

def get_defaultdict_default_default_factory(values_source_type: Any) -> Callable[[], Any]:
    FieldInfo = import_cached_field_info()

    values_type_origin = get_origin(values_source_type)

    def infer_default() -> Callable[[], Any]:
        allowed_default_types: dict[Any, Any] = {
            tuple: tuple,
            collections.abc.Sequence: tuple,
            collections.abc.MutableSequence: list,
            list: list,
            typing.Sequence: list,
            set: set,
            typing.MutableSet: set,
            collections.abc.MutableSet: set,
            collections.abc.Set: frozenset,
            typing.MutableMapping: dict,
            typing.Mapping: dict,
            collections.abc.Mapping: dict,
            collections.abc.MutableMapping: dict,
            float: float,
            int: int,
            str: str,
            bool: bool,
        }
        values_type = values_type_origin or values_source_type
        instructions = 'set using `DefaultDict[..., Annotated[..., Field(default_factory=...)]]`'
        if typing_objects.is_typevar(values_type):

            def type_var_default_factory() -> None:
                raise RuntimeError(
                    'Generic defaultdict cannot be used without a concrete value type or an'
                    ' explicit default factory, ' + instructions
                )

            return type_var_default_factory
        elif values_type not in allowed_default_types:
            # a somewhat subjective set of types that have reasonable default values
            allowed_msg = ', '.join([t.__name__ for t in set(allowed_default_types.values())])
            raise PydanticSchemaGenerationError(
                f'Unable to infer a default factory for keys of type {values_source_type}.'
                f' Only {allowed_msg} are supported, other types require an explicit default factory'
                ' ' + instructions
            )
        return allowed_default_types[values_type]

    # Assume Annotated[..., Field(...)]
    if typing_objects.is_annotated(values_type_origin):
        field_info = next((v for v in get_args(values_source_type) if isinstance(v, FieldInfo)), None)
    else:
        field_info = None
    if field_info and field_info.default_factory:
        # Assume the default factory does not take any argument:
        default_default_factory = cast(Callable[[], Any], field_info.default_factory)
    else:
        default_default_factory = infer_default()
    return default_default_factory

