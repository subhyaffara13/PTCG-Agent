
def _get_inflate_helper_fn_name(
    arg_idx: int,
    input_idx: int,
    function_name: str,
) -> str:
    return f"_inflate_helper_for_{function_name}_input_{input_idx}_arg_{arg_idx}"

