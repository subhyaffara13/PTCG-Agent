
def _resolve_commit_hash_from_cache(storage_folder: Path, revision: str | None) -> str:
    """
    Resolve a commit hash from a cache repo folder and an optional revision.
    """
    if revision and _REGEX_COMMIT_HASH.fullmatch(revision):
        return revision

    refs_dir = storage_folder / "refs"
    snapshots_dir = storage_folder / "snapshots"

    if revision:
        ref_path = refs_dir / revision
        if ref_path.is_file():
            return ref_path.read_text(encoding="utf-8").strip()
        raise ValueError(f"Revision '{revision}' could not be resolved in cache (expected file '{ref_path}').")

    # No revision provided: try common defaults
    main_ref = refs_dir / "main"
    if main_ref.is_file():
        return main_ref.read_text(encoding="utf-8").strip()

    if not snapshots_dir.is_dir():
        raise ValueError(f"Cache repo is missing snapshots directory: {snapshots_dir}. Provide --revision explicitly.")

    candidates = [p.name for p in snapshots_dir.iterdir() if p.is_dir() and _REGEX_COMMIT_HASH.fullmatch(p.name)]
    if len(candidates) == 1:
        return candidates[0]

    raise ValueError(
        "Ambiguous cached revision: multiple snapshots found and no refs to disambiguate. Please pass --revision."
    )

