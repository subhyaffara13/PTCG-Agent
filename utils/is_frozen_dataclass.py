
def is_frozen_dataclass(value: Any) -> bool:
    return (
        not object_has_getattribute(value)
        and not class_has_getattribute(value)
        and is_dataclass(value)
        and hasattr(value, "__dataclass_params__")
        and hasattr(value.__dataclass_params__, "frozen")
        and value.__dataclass_params__.frozen
    )

