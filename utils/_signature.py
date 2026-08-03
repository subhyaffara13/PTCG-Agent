from typing import Any, Dict

def _signature(model) -> inspect.Signature:
    should_be_callable = getattr(model, "forward", model)
    if callable(should_be_callable):
        return inspect.signature(should_be_callable)
    raise ValueError("model has no forward method and is not callable")


def _signature(model) -> inspect.Signature:
    should_be_callable = getattr(model, "forward", model)
    if callable(should_be_callable):
        return inspect.signature(should_be_callable)
    raise ValueError("model has no forward method and is not callable")


def _signature(call: Dict[str, Any]) -> str:
    """Stable signature for loop detection: name + sorted JSON-ish args."""
    name = call.get("name") or call.get("function", {}).get("name", "")
    call_args = call.get("arguments")
    if call_args is None:
        call_args = call.get("function", {}).get("arguments", "")
    if isinstance(call_args, dict):
        call_args = ",".join(f"{k}={call_args[k]}" for k in sorted(call_args.keys()))
    return f"{name}({call_args})"

