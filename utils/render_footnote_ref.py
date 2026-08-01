
def render_footnote_ref(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    ident: str = self.rules["footnote_anchor_name"](tokens, idx, options, env)  # type: ignore[attr-defined]
    caption: str = self.rules["footnote_caption"](tokens, idx, options, env)  # type: ignore[attr-defined]
    refid = ident

    if tokens[idx].meta.get("subId", -1) > 0:
        refid += ":" + str(tokens[idx].meta["subId"])

    return (
        '<sup class="footnote-ref"><a href="#fn'
        + ident
        + '" id="fnref'
        + refid
        + '">'
        + caption
        + "</a></sup>"
    )

