
def _compile_identity_check_function(member: LiteralString, function_name: LiteralString) -> FunctionType:
    """Create a function checking that the function argument is the (unparameterized) typing `member`.

    The function will make sure to check against both the `typing` and `typing_extensions`
    variants as depending on the Python version, the `typing_extensions` variant might be different.
    For instance, on Python 3.9:

    ```pycon
    >>> from typing import Literal as t_Literal
    >>> from typing_extensions import Literal as te_Literal, get_origin

    >>> t_Literal is te_Literal
    False
    >>> get_origin(t_Literal[1])
    typing.Literal
    >>> get_origin(te_Literal[1])
    typing_extensions.Literal
    ```
    """
    in_typing = hasattr(typing, member)
    in_typing_extensions = hasattr(typing_extensions, member)

    if in_typing and in_typing_extensions:
        if getattr(typing, member) is getattr(typing_extensions, member):
            check_code = f'obj is typing.{member}'
        else:
            check_code = f'obj is typing.{member} or obj is typing_extensions.{member}'
    elif in_typing and not in_typing_extensions:
        check_code = f'obj is typing.{member}'
    elif not in_typing and in_typing_extensions:
        check_code = f'obj is typing_extensions.{member}'
    else:
        check_code = 'False'

    func_code = dedent(f"""
    def {function_name}(obj: Any, /) -> bool:
        return {check_code}
    """)

    locals_: dict[str, Any] = {}
    globals_: dict[str, Any] = {'Any': Any, 'typing': typing, 'typing_extensions': typing_extensions}
    exec(func_code, globals_, locals_)
    return locals_[function_name]

