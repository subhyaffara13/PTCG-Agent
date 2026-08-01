
def sub_close(
    renderer: RendererHTML,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    """Render the closing tag for a ~subscript~ token."""
    return "</sub>"

