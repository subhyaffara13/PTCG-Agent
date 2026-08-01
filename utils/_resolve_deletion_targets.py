
def _resolve_deletion_targets(hf_cache_info: HFCacheInfo, targets: list[str]) -> _DeletionResolution:
    """Resolve the deletion targets into a deletion resolution."""
    repo_lookup, revision_lookup = build_cache_index(hf_cache_info)

    selected: dict[CachedRepoInfo, set[CachedRevisionInfo]] = defaultdict(set)
    revisions: set[str] = set()
    missing: list[str] = []

    for raw_target in targets:
        target = raw_target.strip()
        if not target:
            continue
        lowered = target.lower()

        if re.fullmatch(r"[0-9a-fA-F]{40}", lowered):
            match = revision_lookup.get(lowered)
            if match is None:
                missing.append(raw_target)
                continue
            repo, revision = match
            selected[repo].add(revision)
            revisions.add(revision.commit_hash)
            continue

        matched_repo = repo_lookup.get(_repo_cache_id_from_target(target).lower())
        if matched_repo is None:
            missing.append(raw_target)
            continue

        for revision in matched_repo.revisions:
            selected[matched_repo].add(revision)
            revisions.add(revision.commit_hash)

    frozen_selected = {repo: frozenset(revs) for repo, revs in selected.items()}
    return _DeletionResolution(
        revisions=frozenset(revisions),
        selected=frozen_selected,
        missing=tuple(missing),
    )

