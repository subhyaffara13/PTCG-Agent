
def fully_qualified_type(argument_type: str) -> str:
    def maybe_optional_type(type: str, is_opt: bool) -> str:
        return f"std::optional<{type}>" if is_opt else type

    opt_match = OPTIONAL_TYPE_PATTERN.match(argument_type)
    is_opt = opt_match is not None
    if opt_match:
        argument_type = argument_type[opt_match.start(1) : opt_match.end(1)]
    match = TYPE_PATTERN.match(argument_type)
    if match is None:
        return maybe_optional_type(argument_type, is_opt)
    index = match.start(1)
    qualified_type = f"{argument_type[:index]}at::{argument_type[index:]}"
    return maybe_optional_type(qualified_type, is_opt)

