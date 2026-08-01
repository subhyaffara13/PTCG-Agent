
def render_footnote_caption(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    n = str(tokens[idx].meta["id"] + 1)

    if tokens[idx].meta.get("subId", -1) > 0:
        n += ":" + str(tokens[idx].meta["subId"])

    return "[" + n + "]"

