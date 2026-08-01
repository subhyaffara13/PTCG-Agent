
def dataclass_schema(
    cls: type[Any],
    schema: CoreSchema,
    fields: list[str],
    *,
    generic_origin: type[Any] | None = None,
    cls_name: str | None = None,
    post_init: bool | None = None,
    revalidate_instances: Literal['always', 'never', 'subclass-instances'] | None = None,
    strict: bool | None = None,
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
    frozen: bool | None = None,
    slots: bool | None = None,
    config: CoreConfig | None = None,
) -> DataclassSchema:
    """
    Returns a schema for a dataclass. As with `ModelSchema`, this schema can only be used as a field within
    another schema, not as the root type.

    Args:
        cls: The dataclass type, used to perform subclass checks
        schema: The schema to use for the dataclass fields
        fields: Fields of the dataclass, this is used in serialization and in validation during re-validation
            and while validating assignment
        generic_origin: The origin type used for this dataclass, if it's a parametrized generic. Ex,
            if this model schema represents `SomeDataclass[int]`, generic_origin is `SomeDataclass`
        cls_name: The name to use in error locs, etc; this is useful for generics (default: `cls.__name__`)
        post_init: Whether to call `__post_init__` after validation
        revalidate_instances: whether instances of models and dataclasses (including subclass instances)
            should re-validate defaults to config.revalidate_instances, else 'never'
        strict: Whether to require an exact instance of `cls`
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
        frozen: Whether the dataclass is frozen
        slots: Whether `slots=True` on the dataclass, means each field is assigned independently, rather than
            simply setting `__dict__`, default false
    """
    return _dict_not_none(
        type='dataclass',
        cls=cls,
        generic_origin=generic_origin,
        fields=fields,
        cls_name=cls_name,
        schema=schema,
        post_init=post_init,
        revalidate_instances=revalidate_instances,
        strict=strict,
        ref=ref,
        metadata=metadata,
        serialization=serialization,
        frozen=frozen,
        slots=slots,
        config=config,
    )

