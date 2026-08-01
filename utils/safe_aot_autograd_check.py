
def safe_aot_autograd_check(
    op: torch._ops.OpOverload,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    dynamic: bool,
    *,
    copy_inputs: bool = True,
    rtol: float | None = None,
    atol: float | None = None,
) -> Any:
    # NB: copy_inputs does nothing for aot_autograd_check: it always needs to copy
    # inputs.
    if pytree.tree_any_only(torch.Tensor, is_abstract, (args, kwargs)):
        return None

    def func(*args, **kwargs):
        args, kwargs = pytree.tree_map_only(torch.Tensor, torch.clone, (args, kwargs))
        return op(*args, **kwargs)

    # aot_autograd_check runs func(*args, **kwargs) multiple times
    # and assumes `func` does not modify its inputs.
    if rtol and atol:
        assert_equals_fn = functools.partial(
            torch.testing.assert_close, rtol=rtol, atol=atol
        )
    else:
        assert_equals_fn = torch.testing.assert_close
    return aot_autograd_check(
        func,
        args,
        kwargs,
        dynamic,
        check_gradients="auto",
        assert_equals_fn=assert_equals_fn,
    )

