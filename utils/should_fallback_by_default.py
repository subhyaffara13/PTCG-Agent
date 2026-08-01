
def should_fallback_by_default(node: torch.fx.Node) -> bool:
    """Decide whether fallback for a node. This is only used in inductor lite mode."""
    target = node.target

    assert isinstance(
        target, (torch._ops.OpOverload, torch._ops.HigherOrderOperator)
    ), f"Expected OpOverload or HigherOrderOperator, but found {type(target)}"

    if not config.fallback_by_default:
        return False

    # some ops need special handle due to dynamic shapes. we can avoid
    # fallback if they do not impact numerics.
    skip_fallback_due_to_dynamic_shape = OrderedSet(
        [
            torch.ops.aten._assert_scalar.default,
            torch.ops.aten.lift_fresh_copy.default,
        ]
    )

    if target in skip_fallback_due_to_dynamic_shape:
        return False

    # Most hops have registered lowering. We should follow the lowering and not fallback.
    # However, in rare cases, hops may not register lowering, such as
    # torch.ops.higher_order.triton_kernel_wrapper_functional. We should fallback for
    # these hops.
    fallback_hops = OrderedSet(
        [torch.ops.higher_order.triton_kernel_wrapper_functional]
    )

    if isinstance(target, torch._ops.HigherOrderOperator):
        return target in fallback_hops

    return not _needs_inductor_compile(node)

