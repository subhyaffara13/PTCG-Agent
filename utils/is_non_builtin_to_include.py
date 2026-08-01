
def is_non_builtin_to_include(node: fx.Node) -> bool:
    return config.is_non_builtin_to_include and (
        (isinstance(node.target, torch._ops.OpOverload) and not is_builtin(node.target))
        or node.target == torch.ops.higher_order.triton_kernel_wrapper_functional
    )

