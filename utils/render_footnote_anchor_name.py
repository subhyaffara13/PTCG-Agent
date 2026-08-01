
def render_footnote_anchor_name(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    n = str(tokens[idx].meta["id"] + 1)
    prefix = ""

    doc_id = env.get("docId", None)
    if isinstance(doc_id, str):
        prefix = f"-{doc_id}-"

    return prefix + n

