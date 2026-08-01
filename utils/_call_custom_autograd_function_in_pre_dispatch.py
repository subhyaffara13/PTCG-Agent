
def _call_custom_autograd_function_in_pre_dispatch(function_cls_name, *args, **kwargs):
    """
    Import a custom autograd function by string name and call it. This is pretty bad
    because:
    1) There is no schema

    Ideally we should automatically wrap custom autograd functions with a custom op, but
    that is too much work because we need to schematize custom autograd functions. For now,
    we just hackily put it in the IR.
    """
    # Parse module and class name
    module_name, class_name = function_cls_name.rsplit(".", 1)

    # Import the module and get the class
    module = importlib.import_module(module_name)
    function_cls = getattr(module, class_name)
    if not hasattr(function_cls, "apply"):
        raise AssertionError(
            f"Expected function class {function_cls_name} to have 'apply' method"
        )
    return function_cls.apply(*args, **kwargs)

