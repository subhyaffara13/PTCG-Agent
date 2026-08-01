
def invoke_leaf_function_fake(
    real_fn_callable,
    fake_fn_callable,
    input_spec,
    mutated_arg_indices,
    *flat_args,
    requires_grad_indices="",
):
    with unflatten_args_with_modules(flat_args, input_spec) as (args, kwargs):
        return fake_fn_callable(*args, **kwargs)

