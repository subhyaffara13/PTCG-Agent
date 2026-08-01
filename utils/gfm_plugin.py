
def gfm_plugin(
    md: MarkdownIt,
    *,
    dollarmath: bool = False,
    front_matter: bool = False,
    tasklists_editable: bool = False,
) -> None:
    """Enable GFM-like rendering.

    Starts from the current parser configuration and enables the GFM
    components on top.

    :param dollarmath: Enable dollar-delimited math (``$...$``, ``$$...$$``).
    :param front_matter: Enable YAML front matter (``---``).
    :param tasklists_editable: If True, rendered task list checkboxes are not
        disabled (i.e. they are interactive).
    """
    if _parse_version(_mdit_version) < _MIN_VERSION:
        raise RuntimeError(
            f"gfm_plugin requires markdown-it-py >= {'.'.join(str(x) for x in _MIN_VERSION)} "
            f"(installed: {_mdit_version})"
        )

    # Enable table and strikethrough rules (built into markdown-it-py)
    md.enable("table")
    md.enable("strikethrough")

    # GFM options available in markdown-it-py >= 4.1.0
    md.options["tasklists"] = True
    md.options["tasklists_editable"] = tasklists_editable
    md.options["alerts"] = True
    md.options["strikethrough_single_tilde"] = True
    # GFM autolinks
    md.use(gfm_autolink_plugin)

    # Footnotes (inline footnotes ^[...] are not part of GFM)
    md.use(footnote_plugin, inline=False)

    # Dollar math (inline $...$ and block $$...$$)
    if dollarmath:
        md.use(dollarmath_plugin, allow_blank_lines=False)

    # TODO: Tag filter — replace leading `<` with `&lt;` for disallowed raw
    # HTML tags: <title>, <textarea>, <style>, <xmp>, <iframe>, <noembed>,
    # <noframes>, <script>, <plaintext>.
    # See https://github.github.com/gfm/#disallowed-raw-html-extension-

    # Optional plugins
    if front_matter:
        md.use(front_matter_plugin)

