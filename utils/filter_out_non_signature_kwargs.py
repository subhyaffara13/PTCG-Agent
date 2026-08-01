
def filter_out_non_signature_kwargs(extra: list | None = None):
    """
    Decorator to filter out named arguments that are not in the function signature.

    This decorator ensures that only the keyword arguments that match the function's signature, or are specified in the
    `extra` list, are passed to the function. Any additional keyword arguments are filtered out and a warning is issued.

    Parameters:
        extra (`Optional[list]`, *optional*):
            A list of extra keyword argument names that are allowed even if they are not in the function's signature.

    Returns:
        Callable:
            A decorator that wraps the function and filters out invalid keyword arguments.

    Example usage:

        ```python
        @filter_out_non_signature_kwargs(extra=["allowed_extra_arg"])
        def my_function(arg1, arg2, **kwargs):
            print(arg1, arg2, kwargs)

        my_function(arg1=1, arg2=2, allowed_extra_arg=3, invalid_arg=4)
        # This will print: 1 2 {"allowed_extra_arg": 3}
        # And issue a warning: "The following named arguments are not valid for `my_function` and were ignored: 'invalid_arg'"
        ```
    """
    extra = extra or []
    extra_params_to_pass = set(extra)

    def decorator(func):
        sig = inspect.signature(func)
        function_named_args = set(sig.parameters.keys())
        valid_kwargs_to_pass = function_named_args.union(extra_params_to_pass)

        # Required for better warning message
        is_instance_method = "self" in function_named_args
        is_class_method = "cls" in function_named_args

        # Mark function as decorated
        func._filter_out_non_signature_kwargs = True

        @wraps(func)
        def wrapper(*args, **kwargs):
            valid_kwargs = {}
            invalid_kwargs = {}

            for k, v in kwargs.items():
                if k in valid_kwargs_to_pass:
                    valid_kwargs[k] = v
                else:
                    invalid_kwargs[k] = v

            if invalid_kwargs:
                invalid_kwargs_names = [f"'{k}'" for k in invalid_kwargs]
                invalid_kwargs_names = ", ".join(invalid_kwargs_names)

                # Get the class name for better warning message
                if is_instance_method:
                    cls_prefix = args[0].__class__.__name__ + "."
                elif is_class_method:
                    cls_prefix = args[0].__name__ + "."
                else:
                    cls_prefix = ""

                warnings.warn(
                    f"The following named arguments are not valid for `{cls_prefix}{func.__name__}`"
                    f" and were ignored: {invalid_kwargs_names}",
                    UserWarning,
                    stacklevel=2,
                )

            return func(*args, **valid_kwargs)

        return wrapper

    return decorator

