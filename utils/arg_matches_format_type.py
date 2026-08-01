
def arg_matches_format_type(
    arg_type: SuccessfulInferenceResult, format_type: str
) -> bool:
    if format_type in "sr":
        # All types can be printed with %s and %r
        return True
    if isinstance(arg_type, astroid.Instance):
        match arg_type.pytype():
            case "builtins.str":
                return format_type == "c"
            case "builtins.float":
                return format_type in "deEfFgGn%"
            case "builtins.int":
                # Integers allow all types
                return True
        return False
    return True

