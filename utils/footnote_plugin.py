
def footnote_plugin(
    md: MarkdownIt,
    *,
    inline: bool = True,
    move_to_end: bool = True,
    always_match_refs: bool = False,
) -> None:
    """Plugin ported from
    `markdown-it-footnote <https://github.com/markdown-it/markdown-it-footnote>`__.

    It is based on the
    `pandoc definition <http://johnmacfarlane.net/pandoc/README.html#footnotes>`__:

    .. code-block:: md

        Normal footnote:

        Here is a footnote reference,[^1] and another.[^longnote]

        [^1]: Here is the footnote.

        [^longnote]: Here's one with multiple blocks.

            Subsequent paragraphs are indented to show that they
        belong to the previous footnote.

    :param inline: If True, also parse inline footnotes (^[...]).
    :param move_to_end: If True, move footnote definitions to the end of the token stream.
    :param always_match_refs: If True, match references, even if the footnote is not defined.

    """
    md.block.ruler.before(
        "reference", "footnote_def", footnote_def, {"alt": ["paragraph", "reference"]}
    )
    _footnote_ref = partial(footnote_ref, always_match=always_match_refs)
    if inline:
        md.inline.ruler.after("image", "footnote_inline", footnote_inline)
        md.inline.ruler.after("footnote_inline", "footnote_ref", _footnote_ref)
    else:
        md.inline.ruler.after("image", "footnote_ref", _footnote_ref)
    if move_to_end:
        md.core.ruler.after("inline", "footnote_tail", footnote_tail)

    md.add_render_rule("footnote_ref", render_footnote_ref)
    md.add_render_rule("footnote_block_open", render_footnote_block_open)
    md.add_render_rule("footnote_block_close", render_footnote_block_close)
    md.add_render_rule("footnote_open", render_footnote_open)
    md.add_render_rule("footnote_close", render_footnote_close)
    md.add_render_rule("footnote_anchor", render_footnote_anchor)

    # helpers (only used in other rules, no tokens are attached to those)
    md.add_render_rule("footnote_caption", render_footnote_caption)
    md.add_render_rule("footnote_anchor_name", render_footnote_anchor_name)

