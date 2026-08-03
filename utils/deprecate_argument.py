from typing import Any

def deprecate_argument(
    kwargs: dict[str, Any], arg_name: str, default_value=None, *, new_name: str = ""
) -> Any:

    if arg_name in kwargs:
        new_name = new_name or _to_pep8_name(arg_name)
        warnings.warn(
            f"{arg_name!r} argument is deprecated, use {new_name!r}",
            category=PyparsingDeprecationWarning,
            stacklevel=3,
        )
    else:
        kwargs[arg_name] = default_value

    return kwargs[arg_name]


def deprecateArgument(name, msg, category=UserWarning):
    """Raise a warning about deprecated function argument 'name'."""
    warnings.warn("%r is deprecated; %s" % (name, msg), category=category, stacklevel=3)

