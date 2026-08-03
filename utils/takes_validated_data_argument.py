from typing import Any, Callable

def takes_validated_data_argument(
    default_factory: Callable[[], Any] | Callable[[dict[str, Any]], Any],
) -> TypeIs[Callable[[dict[str, Any]], Any]]:
    """Whether the provided default factory callable has a validated data parameter."""
    try:
        sig = _typing_extra.signature_no_eval(default_factory)
    except (ValueError, TypeError):
        # `inspect.signature` might not be able to infer a signature, e.g. with C objects.
        # In this case, we assume no data argument is present:
        return False

    parameters = list(sig.parameters.values())

    return len(parameters) == 1 and can_be_positional(parameters[0]) and parameters[0].default is Parameter.empty

