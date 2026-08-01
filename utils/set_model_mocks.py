
def set_model_mocks(cls: type[BaseModel], undefined_name: str = 'all referenced types') -> None:
    """Set `__pydantic_core_schema__`, `__pydantic_validator__` and `__pydantic_serializer__` to mock core types on a model.

    Args:
        cls: The model class to set the mocks on
        undefined_name: Name of the undefined thing, used in error messages
    """
    undefined_type_error_message = (
        f'`{cls.__name__}` is not fully defined; you should define {undefined_name},'
        f' then call `{cls.__name__}.model_rebuild()`.'
    )

    def attempt_rebuild_fn(attr_fn: Callable[[type[BaseModel]], T]) -> Callable[[], T | None]:
        def handler() -> T | None:
            if cls.model_rebuild(raise_errors=False, _parent_namespace_depth=5) is not False:
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

