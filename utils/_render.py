
def _render(app: Flask, template: Template, context: dict[str, t.Any]) -> str:
    app.update_template_context(context)
    before_render_template.send(
        app, _async_wrapper=app.ensure_sync, template=template, context=context
    )
    rv = template.render(context)
    template_rendered.send(
        app, _async_wrapper=app.ensure_sync, template=template, context=context
    )
    return rv


def _render(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    token = tokens[idx]
    info = unescapeAll(token.info).strip() if token.info else ""
    content = escapeHtml(token.content)
    block_name = ""

    if info:
        block_name = info.split()[0]

    return (
        "<pre><code"
        + (f' class="block-{block_name}" ' if block_name else "")
        + ">"
        + content
        + "</code></pre>\n"
    )

