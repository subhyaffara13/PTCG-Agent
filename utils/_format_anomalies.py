from typing import Any

def _format_anomalies(rows: list[dict[str, Any]]) -> str:
    """Flag variants with high crash or error rates."""
    by_variant: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_variant[r["variant"]].append(r)
    lines: list[str] = []
    for v, rs in sorted(by_variant.items()):
        crashes = sum(
            1 for r in rs
            if str(r["crash_p0"]).lower() == "true"
            or str(r["crash_p1"]).lower() == "true"
        )
        errors = sum(1 for r in rs if r["error"])
        total = len(rs)
        if total == 0:
            continue
        crash_pct = 100.0 * crashes / total
        if crash_pct >= 5.0 or errors > 0:
            lines.append(
                f"- **{v}**: {crashes}/{total} games with crash "
                f"({crash_pct:.1f}%), {errors} hard errors"
            )
    if not lines:
        return "## Anomalies\n\n(none)"
    return "## Anomalies\n\n" + "\n".join(lines)

