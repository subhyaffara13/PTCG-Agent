
def generate_print_python(
    node: ir.FallbackKernel,
    writeline: Callable[[str], None],
) -> None:
    """
    Generate a builtin print call for the print HOP fallback (Python wrapper).

    This function generates Python code that calls the builtin print function
    with format string interpolation.

    Args:
        node: The FallbackKernel IR node representing the print HOP call.
        writeline: A function that writes a line of code to the output buffer.

    Example generated code:
        print('x = {}, y = {}'.format(buf0, buf1))
        print('x = {x}, y = {y}'.format(x=buf0, y=buf1))
        print('x = {}, y = {y}'.format(buf0, y=buf1))
    """
    codegen_args: list[str] = node.codegen_args()
    codegen_kwargs: list[str] = node.codegen_kwargs()

    # First arg is the format string
    if not codegen_args:
        raise ValueError(
            "generate_print_python requires a format string as the first positional argument"
        )
    format_str: str = codegen_args[0]

    # Remaining args are positional arguments for .format()
    positional_args = codegen_args[1:]

    args_str = ", ".join(positional_args + codegen_kwargs)
    writeline(
        f"print({format_str}.format({args_str}))"
        if args_str
        else f"print({format_str})"
    )

