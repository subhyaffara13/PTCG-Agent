
def render_myst_line_comment(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    # Strip leading whitespace from all lines
    content = "\n".join(line.lstrip() for line in tokens[idx].content.split("\n"))
    return f"<!-- {escapeHtml(content)} -->"

