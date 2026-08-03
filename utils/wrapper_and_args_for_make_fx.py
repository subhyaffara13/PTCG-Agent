from typing import Callable

def wrapper_and_args_for_make_fx(
    func: Callable[..., R], args: tuple[object, ...], kwargs: dict[str, object]
) -> tuple[Callable[[list[object]], R], list[object]]:
    # make_fx doesn't support kwargs, so we need to do this flattening
    # and then unflatten the args before calling func
    flat_args, spec = pytree.tree_flatten((args, kwargs))

    def wrapped(flat_args: list[object]) -> R:
        fn_args, fn_kwargs = pytree.tree_unflatten(flat_args, spec)
        return func(*fn_args, **fn_kwargs)

    return wrapped, flat_args

