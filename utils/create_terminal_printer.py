
def create_terminal_printer(
    color: bool, output: TextIO | None = None, error: str = "", success: str = ""
) -> BasicPrinter:
    if color and colorama_unavailable:
        no_colorama_message = (
            "\n"
            "Sorry, but to use --color (color_output) the colorama python package is required.\n\n"
            "Reference: https://pypi.org/project/colorama/\n\n"
            "You can either install it separately on your system or as the colors extra "
            "for isort. Ex: \n\n"
            "$ pip install isort[colors]\n"
        )
        print(no_colorama_message, file=sys.stderr)
        sys.exit(1)

    if not colorama_unavailable:
        colorama.init(strip=False)
    return (
        ColoramaPrinter(error, success, output) if color else BasicPrinter(error, success, output)
    )

