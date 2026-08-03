from typing import Callable

def format_callable_args(
    arg_types: list[Type],
    arg_kinds: list[ArgKind],
    arg_names: list[str | None],
    format: Callable[[Type], str],
    verbosity: int,
) -> str:
    """Format a bunch of Callable arguments into a string"""
    arg_strings = []
    for arg_name, arg_type, arg_kind in zip(arg_names, arg_types, arg_kinds):
        if should_format_arg_as_type(arg_kind, arg_name, verbosity):
            arg_strings.append(format(arg_type))
        else:
            constructor = ARG_CONSTRUCTOR_NAMES[arg_kind]
            if arg_kind.is_star() or arg_name is None:
                arg_strings.append(f"{constructor}({format(arg_type)})")
            else:
                arg_strings.append(f"{constructor}({format(arg_type)}, {repr(arg_name)})")

    return ", ".join(arg_strings)

