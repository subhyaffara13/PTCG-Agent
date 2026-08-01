
def constrain_to_fx_strides(fx_node, *args, **kwargs):
    def apply_constraint(arg, fx_arg):
        if _is_tensor_irnode(arg):
            fake_val = fx_arg.meta.get("val")
            if not isinstance(fake_val, torch.Tensor):
                return arg
            stride_order = ir.get_stride_order(
                fake_val.stride(), V.graph.sizevars.shape_env
            )
            return ir.ExternKernel.require_stride_order(arg, stride_order)
        if isinstance(arg, dict):
            return {key: apply_constraint(arg[key], fx_arg[key]) for key in arg}
        return arg

    args = tuple(
        apply_constraint(arg, fx_arg) for arg, fx_arg in zip(args, fx_node.args)
    )
    kwargs = {k: apply_constraint(v, fx_node.kwargs[k]) for k, v in kwargs.items()}
    return args, kwargs

