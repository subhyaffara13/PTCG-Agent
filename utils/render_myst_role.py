
def render_myst_role(
    self: "RendererProtocol",
    tokens: Sequence["Token"],
    idx: int,
    options: "OptionsDict",
    env: "EnvType",
) -> str:
    token = tokens[idx]
    name = token.meta.get("name", "unknown")
    return f'<code class="myst role">{{{name}}}[{escapeHtml(token.content)}]</code>'

