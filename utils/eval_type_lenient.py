from typing import Any

def eval_type_lenient(
    value: Any,
    globalns: GlobalsNamespace | None = None,
    localns: MappingNamespace | None = None,
) -> Any:
    ev, _ = try_eval_type(value, globalns, localns)
    return ev

