
def gfm_autolink_plugin(md: MarkdownIt) -> None:
    """Enable the GFM autolink extension.

    Recognises bare ``www.`` URLs, ``http(s)://`` URLs,
    ``mailto:``/``xmpp:`` links, and bare email addresses.

    Requires markdown-it-py ≥ 4.1.0.
    """
    if not hasattr(md.inline, "add_terminator_char"):
        raise RuntimeError("gfm_autolink_plugin requires markdown-it-py >= 4.1.0")

    md.inline.add_terminator_char("w")
    md.inline.ruler.push("gfm_autolink_www", _www_inline_rule)
    md.inline.ruler.push("gfm_autolink_protocol", _protocol_rule)
    md.inline.ruler.push("gfm_autolink_email", _email_rule)

