from typing import Any

def _get_args_info_from_callable(
    member: _FunctionTypes,
) -> tuple[list[str], list[str], list[Any], list[str], list[Any]]:
    """Returns args, posonlyargs, defaults, kwonlyargs.

    :note: currently ignores the return annotation.
    """
    signature = inspect.signature(member)
    args: list[str] = []
    defaults: list[Any] = []
    posonlyargs: list[str] = []
    kwonlyargs: list[str] = []
    kwonlydefaults: list[Any] = []

    for param_name, param in signature.parameters.items():
        if param.kind == inspect.Parameter.POSITIONAL_ONLY:
            posonlyargs.append(param_name)
        elif param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            args.append(param_name)
        elif param.kind == inspect.Parameter.VAR_POSITIONAL:
            args.append(param_name)
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            args.append(param_name)
        elif param.kind == inspect.Parameter.KEYWORD_ONLY:
            kwonlyargs.append(param_name)
            if param.default is not inspect.Parameter.empty:
                kwonlydefaults.append(param.default)
            continue
        if param.default is not inspect.Parameter.empty:
            defaults.append(param.default)

    return args, posonlyargs, defaults, kwonlyargs, kwonlydefaults

