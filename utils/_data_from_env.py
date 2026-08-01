
def _data_from_env(env: EnvType) -> _FootnoteData:
    footnotes = env.setdefault("footnotes", {})
    footnotes.setdefault("refs", {})
    footnotes.setdefault("list", {})
    return footnotes  # type: ignore[no-any-return]

