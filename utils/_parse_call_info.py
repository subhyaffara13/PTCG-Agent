
def _parse_call_info(func, args, kwargs, call_argument_expressions, target_args):
    """
    Prepare a string containing the call info to `func`, e.g. argument names/values/expressions.
    """
    signature = inspect.signature(func)
    signature_names = [param.name for param_name, param in signature.parameters.items()]

    # called as `self.method_name()` or `xxx.method_name()`.
    if len(args) == len(call_argument_expressions["positional_args"]) + 1:
        # We simply add "self" as the expression despite it might not be the actual argument name.
        # (This part is very unlikely what a user would be interest to know)
        call_argument_expressions["positional_args"] = ["self"] + call_argument_expressions["positional_args"]

    param_position_mapping = {param_name: idx for idx, param_name in enumerate(signature_names)}

    arg_info = {}
    for arg_name in target_args:
        if arg_name in kwargs:
            arg_value = kwargs[arg_name]
            arg_expr = call_argument_expressions["keyword_args"][arg_name]
        else:
            arg_pos = param_position_mapping[arg_name]
            arg_value = args[arg_pos]
            arg_expr = call_argument_expressions["positional_args"][arg_pos]

        arg_value_str = _format_py_obj(arg_value)
        arg_info[arg_name] = {"arg_expr": arg_expr, "arg_value_str": arg_value_str}

    info = ""
    for arg_name in arg_info:
        arg_expr, arg_value_str = arg_info[arg_name]["arg_expr"], arg_info[arg_name]["arg_value_str"]
        info += f"{'-' * 80}\n\nargument name: `{arg_name}`\nargument expression: `{arg_expr}`\n\nargument value:\n\n{arg_value_str}\n\n"

    # remove the trailing \n\n
    info = info[:-2]

    return info

