
def gen_script_fn_and_args(method_name, func_type, *args, **kwargs):
    formals, tensors, actuals = get_script_args(args)
    call = get_call(method_name, func_type, actuals, kwargs)
    script = script_template.format(', '.join(formals), call)
    CU = torch.jit.CompilationUnit(script)
    return CU.the_method, tensors

