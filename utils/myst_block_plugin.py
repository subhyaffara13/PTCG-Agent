
def myst_block_plugin(md: MarkdownIt) -> None:
    """Parse MyST targets (``(name)=``), blockquotes (``% comment``) and block breaks (``+++``)."""
    md.block.ruler.before(
        "blockquote",
        "myst_line_comment",
        line_comment,
        {"alt": ["paragraph", "reference", "blockquote", "list", "footnote_def"]},
    )
    md.block.ruler.before(
        "hr",
        "myst_block_break",
        block_break,
        {"alt": ["paragraph", "reference", "blockquote", "list", "footnote_def"]},
    )
    md.block.ruler.before(
        "hr",
        "myst_target",
        target,
        {"alt": ["paragraph", "reference", "blockquote", "list", "footnote_def"]},
    )
    md.add_render_rule("myst_target", render_myst_target)
    md.add_render_rule("myst_line_comment", render_myst_line_comment)

