
def _check_for_locals(expr: str, stack_level: int, parser: str) -> None:
    at_top_of_stack = stack_level == 0
    not_pandas_parser = parser != "pandas"

    if not_pandas_parser:
        msg = "The '@' prefix is only supported by the pandas parser"
    elif at_top_of_stack:
        msg = (
            "The '@' prefix is not allowed in top-level eval calls.\n"
            "please refer to your variables by name without the '@' prefix."
        )

    if at_top_of_stack or not_pandas_parser:
        for toknum, tokval in tokenize_string(expr):
            if toknum == tokenize.OP and tokval == "@":
                raise SyntaxError(msg)

