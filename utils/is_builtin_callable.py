
def is_builtin_callable(obj: Any) -> bool:
    # See also torch/_dynamo/polyfills/loader.py, which removes items in _builtin_function_ids
    return id(obj) in _builtin_function_ids

