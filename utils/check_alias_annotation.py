
def check_alias_annotation(method_name, args, kwargs, *, aten_name, func_type='method'):
    formals, tensors, actuals = get_script_args(args)
    call = get_call(method_name, func_type, actuals, kwargs)
    script = script_template.format(', '.join(formals), call)
    CU = torch.jit.CompilationUnit(script)
    # to clean up IR
    torch._C._jit_pass_inline(CU.the_method.graph)
    torch._C._jit_pass_constant_propagation(CU.the_method.graph)
    torch._C._jit_check_alias_annotation(CU.the_method.graph, tuple(tensors), aten_name)

