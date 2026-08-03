from typing import Callable

def register_inference_rule(
    call_target: Target,
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    def register(fn: Callable[_P, _T]) -> Callable[_P, _T]:
        if call_target in _INFERENCE_RULES:
            raise RuntimeError(f"Inference rule already registered for {call_target}!")
        _INFERENCE_RULES[call_target] = fn
        return fn

    return register


def register_inference_rule(
    call_target: Target,
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    def register(fn: Callable[_P, _T]) -> Callable[_P, _T]:
        if call_target in _INFERENCE_RULES:
            raise RuntimeError(f"Inference rule already registered for {call_target}!")
        _INFERENCE_RULES[call_target] = fn  # pyrefly: ignore[unsupported-operation]
        return fn

    return register

