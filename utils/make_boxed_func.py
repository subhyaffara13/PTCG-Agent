from typing import Any, Callable

def make_boxed_func(f: Callable[..., Any]) -> Callable[[list[Any]], Any]:
    @simple_wraps(f)
    def g(args: list[Any]) -> Any:
        return f(*args)

    # pyrefly: ignore[missing-attribute]
    g._boxed_call = True
    return g

