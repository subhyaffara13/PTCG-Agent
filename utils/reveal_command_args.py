
def reveal_command_args(args: list[str] | CommandArgs) -> list[str]:
    """
    Return the arguments in their raw, unredacted form.
    """
    return [arg.secret if isinstance(arg, HiddenText) else arg for arg in args]

