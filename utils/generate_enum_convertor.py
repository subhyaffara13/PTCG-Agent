from typing import Any, Callable

def generate_enum_convertor(enum: type[Enum]) -> Callable[[Any], Any]:
    val_map = {str(val.value): val for val in enum}

    def convertor(value: Any) -> Any:
        if value is not None:
            val = str(value)
            if val in val_map:
                key = val_map[val]
                return enum(key)

    return convertor

