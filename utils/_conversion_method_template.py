from typing import Any, Callable

def _conversion_method_template(**extra_kwargs: Any) -> Callable[..., Any]:
    def _(self: FunctionalTensor, *args: Any, **kwargs: Any) -> Any:
        return self.to(*args, **{**kwargs, **extra_kwargs})

    return _

