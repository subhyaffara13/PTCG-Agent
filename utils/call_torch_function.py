from typing import Any, Callable

def call_torch_function(
    tx: "InstructionTranslator",
    torch_function_var: VariableTracker,
    fn: VariableTracker,
    types: TupleVariable,
    args: Iterable[Any],
    kwargs: dict[str, Any],
    *,
    is_subclass_dispatch: bool = False,
) -> Any:
    # This emulates calling __torch_function__, which has a signature
    #   def __torch_function__(cls, func, types, args=(), kwargs=None):
    #
    # Also notice the `cls` is not explicitly passed in the reference
    # implementations:
    # 1. https://github.com/pytorch/pytorch/blob/8d81806211bc3c0ee6c2ef235017bacf1d775a85/torch/csrc/utils/python_arg_parser.cpp#L368-L374  # noqa: B950
    # 2. https://github.com/pytorch/pytorch/blob/8d81806211bc3c0ee6c2ef235017bacf1d775a85/torch/overrides.py#L1741-L1743
    tf_args = [
        fn,
        types,
        VariableTracker.build(tx, tuple(args)),
        VariableTracker.build(tx, kwargs),
    ]
    # Mirror the C++ THPModule_disable_torch_function behavior: disable
    # __torch_function__ subclass dispatch during the call to prevent
    # re-entrant dispatch on operations inside __torch_function__.
    # Only do this for subclass dispatch, not mode dispatch. Modes need
    # subclass dispatch to remain enabled because the mode's
    # __torch_function__ may re-dispatch to the subclass.
    tf_state = tx.symbolic_torch_function_state
    old_subclass_enabled = tf_state.torch_function_subclass_enabled
    if is_subclass_dispatch and old_subclass_enabled:
        tf_state.torch_function_subclass_enabled = False
    try:
        return torch_function_var.call_function(tx, tf_args, {})
    finally:
        tf_state.torch_function_subclass_enabled = old_subclass_enabled


def call_torch_function(
    wrapper: WrappedOperator,
    func: Callable,
    types: tuple,
    args: tuple = (),
    kwargs: dict | None = None,
) -> Any:
    """
    Handle __torch_function__ calls for wrapped operators.
    """
    if kwargs is None:
        kwargs = {}

    # Import here to avoid circular imports
    from . import _Tensor

    # Use the torch function mechanism from _Tensor
    return _Tensor.__torch_function__(func, types, args, kwargs)

