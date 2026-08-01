
def emit_noargs_leaf_function_to_graph(
    tx: "InstructionTranslator",
    real_impl: Callable[[], None],
    name: str,
) -> None:
    """Emit an invoke_leaf_function node for a side-effectful function with no
    tensor inputs or outputs.

    The function is captured as a closure inside _LeafCallable objects and
    registered as a static attribute on the graph module.  Because
    invoke_leaf_function is registered as EffectType.ORDERED, effect tokens
    prevent DCE and maintain execution ordering relative to other ops.

    Use this when Dynamo needs to preserve a pure-side-effect call (like
    setting global runtime state) in the compiled graph so that it replays
    at the correct position at runtime.
    """
    import torch.utils._pytree as pytree
    from torch._higher_order_ops.invoke_leaf_function import (
        _LeafCallable,
        invoke_leaf_function,
        make_leaf_function_wrappers,
    )

    def fake_impl():
        return None

    captured_out_spec: list[pytree.TreeSpec | None] = [None]
    wrapped_real, wrapped_fake = make_leaf_function_wrappers(
        real_impl, fake_impl, captured_out_spec
    )

    real_callable = _LeafCallable(wrapped_real)
    fake_callable = _LeafCallable(wrapped_fake)
    input_spec = pytree.tree_flatten(((), {}))[1]

    def make_proxy(attr_name: str, val: Any) -> Any:
        proxy = tx.output.register_static_attr_and_return_proxy(attr_name, val)
        proxy.node.type = type(val)
        return proxy

    invoke_args = (
        make_proxy(f"{name}_real_fn", real_callable),
        make_proxy(f"{name}_fake_fn", fake_callable),
        make_proxy(f"{name}_input_spec", input_spec),
        "",  # mutated_flat_indices
    )
    tx.output.create_proxy("call_function", invoke_leaf_function, invoke_args, {})

