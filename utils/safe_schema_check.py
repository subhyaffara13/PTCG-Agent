
def safe_schema_check(
    op: torch._ops.OpOverload,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    *,
    copy_inputs: bool = True,
    rtol: float | None = None,
    atol: float | None = None,
) -> Any:
    if copy_inputs:
        args, kwargs = deepcopy_tensors((args, kwargs))
    if pytree.tree_any_only(torch.Tensor, is_abstract, (args, kwargs)):
        return None
    with SchemaCheckMode():
        result = op(*args, **kwargs)
        return result

