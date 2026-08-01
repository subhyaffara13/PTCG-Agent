
def data_dep(
    fake_mode: FakeTensorMode, func: OpOverload, *args: Any, **kwargs: Any
) -> None:
    raise DataDependentOutputException(func)

