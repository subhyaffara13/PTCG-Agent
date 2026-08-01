
def is_instance_method_from_sig(function: AnyDecoratorCallable) -> bool:
    """Whether the function is an instance method.

    It will consider a function as instance method if the first parameter of
    function is `self`.

    Args:
        function: The function to check.

    Returns:
        `True` if the function is an instance method, `False` otherwise.
    """
    sig = signature_no_eval(unwrap_wrapped_function(function))
    first = next(iter(sig.parameters.values()), None)
    if first and first.name == 'self':
        return True
    return False

