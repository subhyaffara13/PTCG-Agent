from typing import Any, Callable, Dict, Optional, Tuple

def convert_args_to_kwargs(
    original_function: Callable,
    args: Optional[Tuple[Any, ...]] = None,
) -> Dict[str, Any]:
    # Get the signature of the original function
    signature = inspect.signature(original_function)

    # Get parameter names in the order they appear in the original function
    param_names = list(signature.parameters.keys())

    # Create a mapping of positional arguments to parameter names
    args_to_kwargs = {}
    if args:
        for index, arg in enumerate(args):
            if index < len(param_names):
                param_name = param_names[index]
                args_to_kwargs[param_name] = arg

    return args_to_kwargs

