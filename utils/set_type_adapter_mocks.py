from typing import Callable

def set_type_adapter_mocks(adapter: TypeAdapter) -> None:
    """Set `core_schema`, `validator` and `serializer` to mock core types on a type adapter instance.

    Args:
        adapter: The type adapter instance to set the mocks on
    """
    type_repr = str(adapter._type)
    undefined_type_error_message = (
        f'`TypeAdapter[{type_repr}]` is not fully defined; you should define `{type_repr}` and all referenced types,'
        f' then call `.rebuild()` on the instance.'
    )

    def attempt_rebuild_fn(attr_fn: Callable[[TypeAdapter], T]) -> Callable[[], T | None]:
        def handler() -> T | None:
            if adapter.rebuild(raise_errors=False, _parent_namespace_depth=5) is not False:
                return attr_fn(adapter)
            return None

        return handler

    adapter.core_schema = MockCoreSchema(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        attempt_rebuild=attempt_rebuild_fn(lambda ta: ta.core_schema),
    )
    adapter.validator = MockValSer(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        val_or_ser='validator',
        attempt_rebuild=attempt_rebuild_fn(lambda ta: ta.validator),
    )
    adapter.serializer = MockValSer(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        val_or_ser='serializer',
        attempt_rebuild=attempt_rebuild_fn(lambda ta: ta.serializer),
    )

