from typing import Any

def temporarily_restore_interpreter_stack(
    stack: list[Any] | None,
) -> Generator[None, None, None]:
    pushed: list[Any] = []
    if stack is None:
        return
    try:
        for s in reversed(stack):
            push_dynamic_layer_stack(s)
            pushed.append(s)
        yield
    finally:
        for _ in reversed(pushed):
            # TODO: would be nice to assert that the layers are the same, but
            # Python object identity is not preserved
            pop_dynamic_layer_stack()

