from typing import Callable

def register_transformation_rule(
    call_target: type[Constraint],
) -> Callable[[_TransformFn], _TransformFn]:
    def register(fn: _TransformFn) -> _TransformFn:
        if call_target in _TRANSFORMATION_RULES:
            raise RuntimeError(
                f"Transformation rule already registered for {call_target}!"
            )
        _TRANSFORMATION_RULES[call_target] = fn
        return fn

    return register

