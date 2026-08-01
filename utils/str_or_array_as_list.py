
def str_or_array_as_list(v: str | Sequence[str]) -> list[str]:
    if isinstance(v, str):
        return [v.strip()] if v.strip() else []
    return [p.strip() for p in v if p.strip()]

