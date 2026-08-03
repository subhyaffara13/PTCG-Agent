from typing import Any, Callable

def createResolutionCallbackFromClosure(fn) -> Callable[[str], Any]:
    """
    Create a resolutionCallback by introspecting the function instead of
    looking up the stack for the enclosing scope
    """
    closure = get_closure(fn)

    class closure_lookup:
        # This is a class since `closure` is a dict and it's easier in
        # `env_helper` if everything just works with `getattr` calls
        def __getattr__(self, key: str) -> Any:
            if key in closure:
                return closure[key]
            elif hasattr(typing, key):
                return getattr(typing, key)
            elif hasattr(builtins, key):
                return getattr(builtins, key)
            return None

    return createResolutionCallbackFromEnv(closure_lookup())

