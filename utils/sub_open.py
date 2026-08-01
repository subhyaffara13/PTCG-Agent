
def sub_open(
    renderer: RendererHTML,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    """Render the opening tag for a ~subscript~ token."""
    return "<sub>"

