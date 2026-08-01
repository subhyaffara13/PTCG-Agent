
def render_footnote_anchor(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    ident: str = self.rules["footnote_anchor_name"](tokens, idx, options, env)  # type: ignore[attr-defined]

    if tokens[idx].meta["subId"] > 0:
        ident += ":" + str(tokens[idx].meta["subId"])

    # ↩ with escape code to prevent display as Apple Emoji on iOS
    return ' <a href="#fnref' + ident + '" class="footnote-backref">\u21a9\ufe0e</a>'

