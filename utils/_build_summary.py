
def _build_summary(
    repos: list[RepoStorageInfo],
    total_storage: int,
    extra_count: int,
) -> list[str]:
    lines: list[str] = [""]
    lines.append("  Storage Overview")
    lines.append("  " + "─" * 16)
    lines.append(f"  {format_size(total_storage, human_readable=True)} total")
    lines.append("")

    order = ["model", "dataset", "space", "bucket"]
    labels = {"model": "Models", "dataset": "Datasets", "space": "Spaces", "bucket": "Buckets"}
    for rtype in order:
        group = [r for r in repos if r.type == rtype]
        if not group:
            continue
        storage = sum(r.storage for r in group)
        sq = _colored_square(_TYPE_COLORS[rtype][0])
        lines.append(f"  {sq} {labels[rtype]}")
        lines.append(f"    {len(group)} repos · {format_size(storage, human_readable=True)}")
        lines.append("")

    if extra_count > 0:
        sq = _colored_square(_EXTRA_COLORS[0])
        lines.append(f"  {sq} +{extra_count} more repos")

    return lines

