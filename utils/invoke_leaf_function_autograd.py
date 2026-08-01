
def invoke_leaf_function_autograd(
    real_fn_callable,
    fake_fn_callable,
    input_spec,
    mutated_arg_indices,
    *flat_args,
    requires_grad_indices="",
):
    return InvokeLeafFunctionAutogradOp.apply(
        real_fn_callable, fake_fn_callable, input_spec, mutated_arg_indices, *flat_args
    )

