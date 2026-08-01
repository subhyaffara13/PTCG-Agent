
def evaluate_call(call, parent, ignore_nodes=None):
    secure = False
    evaluate = False
    if isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute):
        if (
            isinstance(call.func.value, ast.Constant)
            and call.func.attr == "format"
        ):
            evaluate = True
            if call.keywords:
                evaluate = False  # TODO(??) get support for this

    if evaluate:
        args = list(call.args)
        num_secure = 0
        for arg in args:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                num_secure += 1
            elif isinstance(arg, ast.Name):
                if evaluate_var(arg, parent, call.lineno, ignore_nodes):
                    num_secure += 1
                else:
                    break
            elif isinstance(arg, ast.Call):
                if evaluate_call(arg, parent, ignore_nodes):
                    num_secure += 1
                else:
                    break
            elif isinstance(arg, ast.Starred) and isinstance(
                arg.value, (ast.List, ast.Tuple)
            ):
                args.extend(arg.value.elts)
                num_secure += 1
            else:
                break
        secure = num_secure == len(args)

    return secure

