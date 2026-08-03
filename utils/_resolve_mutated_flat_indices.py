from typing import Any, Callable

def _resolve_mutated_flat_indices(
    fn: Callable,
    mutates_args: frozenset[str],
    num_flat_args: int,
    input_spec: pytree.TreeSpec,
) -> str:
    """Resolve mutates_args expressions to a comma-separated string of flat-arg indices.

    Each expression in mutates_args (e.g. "x", "model.running_mean") is evaluated
    against sentinel values to determine which flat-arg positions are mutated.

    Example: for ``def fn(x, model)`` where model is an nn.Module with parameters
    ``weight`` and ``bias``, the flat args are ``[x, nn_module_index, weight, bias]``.
    Given ``mutates_args={"model.weight"}``, this assigns sentinels ``[0, 1, 2, 3]``
    to the flat args, evaluates ``model.weight`` to ``2``, and returns ``"2"``.
    """
    import inspect

    class _AttrDict:
        pass

    def _set_nested_attr(obj: _AttrDict, fqn: str, value: Any) -> None:
        parts = fqn.split(".")
        for part in parts[:-1]:
            if not hasattr(obj, part):
                setattr(obj, part, _AttrDict())
            obj = getattr(obj, part)
        setattr(obj, parts[-1], value)

    def _lms_to_attr_dict(val: Any) -> Any:
        if isinstance(val, LeafModuleState):
            target = _AttrDict()
            for fqn, sentinel in val.named_parameters.items():
                _set_nested_attr(target, fqn, sentinel)
            for fqn, sentinel in val.named_buffers.items():
                _set_nested_attr(target, fqn, sentinel)
            return target
        return val

    sig = inspect.signature(fn)
    sentinels = list(range(num_flat_args))
    args_struct, kwargs_struct = pytree.tree_unflatten(sentinels, input_spec)
    args_eval, kwargs_eval = pytree.tree_map(
        _lms_to_attr_dict,
        (args_struct, kwargs_struct),
        is_leaf=lambda x: isinstance(x, LeafModuleState),
    )
    namespace = dict(sig.bind(*args_eval, **kwargs_eval).arguments)

    indices: list[int] = []
    for expr in mutates_args:
        # Empty __builtins__ prevents access to builtins like __import__, open, exec.
        result = eval(expr, {"__builtins__": {}}, namespace)  # noqa: S307
        leaves = pytree.tree_leaves(result)
        for sentinel in leaves:
            if not isinstance(sentinel, int):
                raise ValueError(
                    f"mutates_args expression '{expr}' resolved to a non-leaf value "
                    f"of type {type(sentinel).__name__}. Expressions must resolve to "
                    f"individual tensor positions, e.g. 'model.weight' not 'model'."
                )
            indices.append(sentinel)
    indices.sort()
    return ",".join(str(i) for i in indices)

