
def _get_torch_jit_trace_forward_signature(mod: torch.nn.Module) -> inspect.Signature:
    """
    Get source code and parse argument names using AST. The function returns
    a signature of the forward() function.

    # TODO: Directly provide inspect.signature compatible TS-d module.
    """
    ast_mod = ast.parse(mod.code)  # type: ignore[call-overload]
    ast_func_def: ast.FunctionDef = ast_mod.body[0]

    # FIXME(jiashenc): TorchScript should only allow positional or keywords arguments.
    arg_type_map = {"args": Parameter.POSITIONAL_OR_KEYWORD}

    # Traverse all argument types in AST tree and create associated parameters.
    param_list = []
    for arg_type, param_type in arg_type_map.items():
        arg_name_list = [a.arg for a in getattr(ast_func_def.args, arg_type)]
        for arg_name in arg_name_list:
            if arg_name == "self":
                continue  # Skip self argument.
            param_list.append(inspect.Parameter(arg_name, param_type))

    return inspect.Signature(parameters=param_list)

