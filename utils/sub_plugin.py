
def sub_plugin(md: MarkdownIt) -> None:
    """
    Markdown-it-py plugin to introduce <sub> markup using ~subscript~.

    Ported from
    https://github.com/markdown-it/markdown-it-sub/blob/master/index.mjs

    Originally ported during implementation of https://github.com/hasgeek/funnel/blob/main/funnel/utils/markdown/mdit_plugins/sub_tag.py
    """
    md.inline.ruler.after("emphasis", "sub", tokenize)
    md.add_render_rule("sub_open", sub_open)
    md.add_render_rule("sub_close", sub_close)

