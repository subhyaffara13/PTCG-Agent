from typing import Any

def enum(validator, enums, instance, schema):
    if all(not equal(each, instance) for each in enums):
        yield ValidationError(f"{instance!r} is not one of {enums!r}")


def enum(*sequential: Any, **named: Any) -> type[Any]:
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = {value: key for key, value in enums.items()}
    enums["reverse_mapping"] = reverse
    return type("Enum", (), enums)

