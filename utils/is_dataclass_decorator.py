
def is_dataclass_decorator(d: Expression) -> bool:
    return dataclass_decorator_type(d) is not None

