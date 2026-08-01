
def set_dataclass_mocks(cls: type[PydanticDataclass], undefined_name: str = 'all referenced types') -> None:
    """Set `__pydantic_validator__` and `__pydantic_serializer__` to `MockValSer`s on a dataclass.

    Args:
        cls: The model class to set the mocks on
        undefined_name: Name of the undefined thing, used in error messages
    """
    from ..dataclasses import rebuild_dataclass

    undefined_type_error_message = (
        f'`{cls.__name__}` is not fully defined; you should define {undefined_name},'
        f' then call `pydantic.dataclasses.rebuild_dataclass({cls.__name__})`.'
    )

    def attempt_rebuild_fn(attr_fn: Callable[[type[PydanticDataclass]], T]) -> Callable[[], T | None]:
        def handler() -> T | None:
            if rebuild_dataclass(cls, raise_errors=False, _parent_namespace_depth=5) is not False:
                return attr_fn(cls)
            return None

        return handler

    cls.__pydantic_core_schema__ = MockCoreSchema(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        attempt_rebuild=attempt_rebuild_fn(lambda c: c.__pydantic_core_schema__),
    )
    cls.__pydantic_validator__ = MockValSer(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        val_or_ser='validator',
        attempt_rebuild=attempt_rebuild_fn(lambda c: c.__pydantic_validator__),
    )
    cls.__pydantic_serializer__ = MockValSer(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        val_or_ser='serializer',
        attempt_rebuild=attempt_rebuild_fn(lambda c: c.__pydantic_serializer__),
    )

