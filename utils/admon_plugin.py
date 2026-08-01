
def admon_plugin(md: MarkdownIt, render: None | Callable[..., str] = None) -> None:
    """Plugin to use
    `python-markdown style admonitions
    <https://python-markdown.github.io/extensions/admonition>`_.

    .. code-block:: md

        !!! note
            *content*

    `And mkdocs-style collapsible blocks
    <https://squidfunk.github.io/mkdocs-material/reference/admonitions/#collapsible-blocks>`_.

    .. code-block:: md

        ???+ note
            *content*

    Note, this is ported from
    `markdown-it-admon
    <https://github.com/commenthol/markdown-it-admon>`_.
    """

    def renderDefault(
        self: RendererProtocol,
        tokens: Sequence[Token],
        idx: int,
        _options: OptionsDict,
        env: EnvType,
    ) -> str:
        return self.renderToken(tokens, idx, _options, env)  # type: ignore[attr-defined,no-any-return]

    render = render or renderDefault

    md.add_render_rule("admonition_open", render)
    md.add_render_rule("admonition_close", render)
    md.add_render_rule("admonition_title_open", render)
    md.add_render_rule("admonition_title_close", render)

    md.block.ruler.before(
        "fence",
        "admonition",
        admonition,
        {"alt": ["paragraph", "reference", "blockquote", "list"]},
    )

