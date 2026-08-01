
def colon_fence_plugin(md: MarkdownIt) -> None:
    """This plugin directly mimics regular fences, but with `:` colons.

    Example::

        :::name
        contained text
        :::

    """

    md.block.ruler.before(
        "fence",
        "colon_fence",
        _rule,
        {"alt": ["paragraph", "reference", "blockquote", "list", "footnote_def"]},
    )
    md.add_render_rule("colon_fence", _render)

