from typing import Callable

def register_refinement_rule(
    call_target: Target,
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    def register(fn: Callable[_P, _T]) -> Callable[_P, _T]:
        if call_target in _REFINEMENT_RULES:
            raise RuntimeError(f"Refinement rule already registered for {call_target}!")
        _REFINEMENT_RULES[call_target] = fn
        return fn

    return register

