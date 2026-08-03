from typing import Any, Callable

def lookup_callable(obj: Callable[..., Any]) -> type[VariableTracker] | None:
    if not hashable(obj):
        return None
    # Custom allow/disallow in graph takes precedence over the general lookup.
    if is_callable_disallowed(obj):
        return SkipFunctionVariable
    if is_callable_allowed(obj):
        return TorchInGraphFunctionVariable
    if is_polyfilled_callable(obj):
        return PolyfilledFunctionVariable
    if obj in BUILTIN_CALLABLES:
        return BUILTIN_CALLABLES[obj]
    if is_builtin_callable(obj):
        return BuiltinVariable
    return None

