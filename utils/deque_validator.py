from typing import Any

def deque_validator(v: Any) -> Deque[Any]:
    if isinstance(v, deque):
        return v
    elif sequence_like(v):
        return deque(v)
    else:
        raise errors.DequeError()


def deque_validator(input_value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> collections.deque[Any]:
    return collections.deque(handler(input_value), maxlen=getattr(input_value, 'maxlen', None))

