
def _compile_isinstance_check_function(member: LiteralString, function_name: LiteralString) -> FunctionType:
    """Create a function checking that the function is an instance of the typing `member`.

    The function will make sure to check against both the `typing` and `typing_extensions`
    variants as depending on the Python version, the `typing_extensions` variant might be different.
    """
    in_typing = hasattr(typing, member)
    in_typing_extensions = hasattr(typing_extensions, member)

    if in_typing and in_typing_extensions:
        if getattr(typing, member) is getattr(typing_extensions, member):
            check_code = f'isinstance(obj, typing.{member})'
        else:
            check_code = f'isinstance(obj, (typing.{member}, typing_extensions.{member}))'
    elif in_typing and not in_typing_extensions:
        check_code = f'isinstance(obj, typing.{member})'
    elif not in_typing and in_typing_extensions:
        check_code = f'isinstance(obj, typing_extensions.{member})'
    else:
        check_code = 'False'

    func_code = dedent(f"""
    def {function_name}(obj: Any, /) -> 'TypeIs[{member}]':
        return {check_code}
    """)

    locals_: dict[str, Any] = {}
    globals_: dict[str, Any] = {'Any': Any, 'typing': typing, 'typing_extensions': typing_extensions}
    exec(func_code, globals_, locals_)
    return locals_[function_name]

