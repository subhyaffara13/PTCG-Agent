
def get_meta_ex_name(meta_name: str) -> str:
    # Convert e.g. foo.bar.meta.ff to foo.bar.meta_ex.ff
    parts = meta_name.rsplit(".", maxsplit=2)
    parts[1] = "meta_ex"
    return ".".join(parts)

