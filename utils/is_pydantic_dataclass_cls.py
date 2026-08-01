
def is_pydantic_dataclass_cls(value: object) -> bool:
    return (
        inspect.isclass(value)
        and dataclasses.is_dataclass(value)
        and "__is_pydantic_dataclass__" in getattr(value, "__dict__", {})
    )

