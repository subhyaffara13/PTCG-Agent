
def render_myst_target(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    label = tokens[idx].content
    class_name = "myst-target"
    target = f'<a href="#{label}">({label})=</a>'
    return f'<div class="{class_name}">{target}</div>'

