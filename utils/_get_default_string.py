from typing import Any, Callable, Union

def _get_default_string(
    obj: Union["TyperArgument", "TyperOption"],
    *,
    ctx: click.Context,
    show_default_is_str: bool,
    default_value: list[Any] | tuple[Any, ...] | str | Callable[..., Any] | Any,
) -> str:
    # Extracted from click.core.Option.get_help_record() to be reused by
    # rich_utils avoiding RegEx hacks
    if show_default_is_str:
        default_string = f"({obj.show_default})"
    elif isinstance(default_value, (list, tuple)):
        default_string = ", ".join(
            _get_default_string(
                obj, ctx=ctx, show_default_is_str=show_default_is_str, default_value=d
            )
            for d in default_value
        )
    elif isinstance(default_value, Enum):
        default_string = str(default_value.value)
    elif inspect.isfunction(default_value):
        default_string = _("(dynamic)")
    elif isinstance(obj, TyperOption) and obj.is_bool_flag and obj.secondary_opts:
        # For boolean flags that have distinct True/False opts,
        # use the opt without prefix instead of the value.
        # Typer override, original commented
        # default_string = click.parser.split_opt(
        #     (self.opts if self.default else self.secondary_opts)[0]
        # )[1]
        if obj.default:
            if obj.opts:
                default_string = _split_opt(obj.opts[0])[1]
            else:
                default_string = str(default_value)
        else:
            default_string = _split_opt(obj.secondary_opts[0])[1]
        # Typer override end
    elif (
        isinstance(obj, TyperOption)
        and obj.is_bool_flag
        and not obj.secondary_opts
        and not default_value
    ):
        default_string = ""
    else:
        default_string = str(default_value)
    return default_string

