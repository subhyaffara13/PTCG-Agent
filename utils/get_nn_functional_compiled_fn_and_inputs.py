
def get_nn_functional_compiled_fn_and_inputs(name, self_size, args, variant_name='', *extra_args):
    test_name = 'test_nn_' + name

    if variant_name != '':
        test_name = test_name + '_' + variant_name

    self_variable = create_input((self_size,))[0][0]

    # need to record this because methods can change the size (e.g. unsqueeze)
    args_variable, _kwargs_variable = create_input(args)

    self_tensor = deepcopy(self_variable.data)
    args_tensor = deepcopy(unpack_variables(args_variable))

    f_args_variable = (self_variable,) + args_variable
    f_args_tensor = (self_tensor,) + args_tensor  # noqa: F841
    with torch._jit_internal._disable_emit_hooks():
        script_fn, inputs = gen_script_fn_and_args(name, "nn_functional", *f_args_variable)
    return script_fn, inputs

