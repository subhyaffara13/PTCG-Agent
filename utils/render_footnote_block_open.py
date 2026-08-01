
def render_footnote_block_open(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    return (
        (
            '<hr class="footnotes-sep" />\n'
            if options.xhtmlOut
            else '<hr class="footnotes-sep">\n'
        )
        + '<section class="footnotes">\n'
        + '<ol class="footnotes-list">\n'
    )

