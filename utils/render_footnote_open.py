
def render_footnote_open(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    ident: str = self.rules["footnote_anchor_name"](tokens, idx, options, env)  # type: ignore[attr-defined]

    if tokens[idx].meta.get("subId", -1) > 0:
        ident += ":" + tokens[idx].meta["subId"]

    return '<li id="fn' + ident + '" class="footnote-item">'

