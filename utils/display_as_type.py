from typing import Any

def display_as_type(v: Type[Any]) -> str:
    if not isinstance(v, typing_base) and not isinstance(v, WithArgsTypes) and not isinstance(v, type):
        v = v.__class__

    if is_union(get_origin(v)):
        return f'Union[{", ".join(map(display_as_type, get_args(v)))}]'

    if isinstance(v, WithArgsTypes):
        # Generic alias are constructs like `list[int]`
        return str(v).replace('typing.', '')

    try:
        return v.__name__
    except AttributeError:
        # happens with typing objects
        return str(v).replace('typing.', '')


def display_as_type(obj: Any) -> str:
    """Pretty representation of a type, should be as close as possible to the original type definition string.

    Takes some logic from `typing._type_repr`.
    """
    if isinstance(obj, (types.FunctionType, types.BuiltinFunctionType)):
        return obj.__name__
    elif obj is ...:
        return '...'
    elif isinstance(obj, Representation):
        return repr(obj)
    elif isinstance(obj, ForwardRef) or typing_objects.is_typealiastype(obj):
        return str(obj)

    if not isinstance(obj, (_typing_extra.typing_base, _typing_extra.WithArgsTypes, type)):
        obj = obj.__class__

    if is_union_origin(typing_extensions.get_origin(obj)):
        args = ', '.join(map(display_as_type, typing_extensions.get_args(obj)))
        return f'Union[{args}]'
    elif isinstance(obj, _typing_extra.WithArgsTypes):
        if typing_objects.is_literal(typing_extensions.get_origin(obj)):
            args = ', '.join(map(repr, typing_extensions.get_args(obj)))
        else:
            args = ', '.join(map(display_as_type, typing_extensions.get_args(obj)))
        try:
            return f'{obj.__qualname__}[{args}]'
        except AttributeError:
            return str(obj).replace('typing.', '').replace('typing_extensions.', '')  # handles TypeAliasType in 3.12
    elif isinstance(obj, type):
        return obj.__qualname__
    else:
        return repr(obj).replace('typing.', '').replace('typing_extensions.', '')

