
def embed_headers(
    fname: str, include_dirs: Sequence[str] | Sequence[Path] | str | None = None
) -> str:
    if include_dirs is None:
        base_dir = Path(__file__).parent.parent.parent
        include_dirs = [base_dir, base_dir / "aten" / "src"]
    elif isinstance(include_dirs, str):
        include_dirs = [Path(include_dirs)]
    else:
        include_dirs = [Path(x) for x in include_dirs]

    return _embed_headers(read_file(fname), include_dirs, {fname})

