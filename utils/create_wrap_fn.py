
def create_wrap_fn(
    fn: Callable[..., Any], args: tuple[Any, ...]
) -> tuple[Callable[..., Any], tuple[Any, ...]]:
    from torch.fx.experimental.proxy_tensor import maybe_enable_thunkify

    from .functional_utils import from_fun, has_data_mutation, to_fun

    def assert_no_mutation(t: Any) -> None:
        if has_data_mutation(t):
            raise AssertionError(
                "Saved tensors hooks with inputs mutations are not allowed"
            )

    @simple_wraps(fn)
    def _wrapper(*args: Any) -> Any:
        with maybe_enable_thunkify():
            disable_above = torch._C._ExcludeDispatchKeyGuard(
                torch._C.DispatchKeySet(torch._C.DispatchKey.Functionalize)
            )

            with disable_above:
                f_args = pytree.tree_map(to_fun, args)
                f_outs = fn(*f_args)
                pytree.tree_map(assert_no_mutation, f_args)
                return pytree.tree_map(from_fun, f_outs)

    return _wrapper, args

