
def register_algebraic_expressions_inference_rule(
    call_target: Target,
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    def register(fn: Callable[_P, _T]) -> Callable[_P, _T]:
        if call_target in _RULES:
            raise RuntimeError(f"Rule already registered for {call_target}!")
        _RULES[call_target] = fn
        return fn

    return register

