
def format_fetch_summary(addrs: list[str], resps: list[Response]) -> str | None:
    """Return a summary string if any workers failed, or None if all succeeded."""
    failed = [(i, r) for i, r in enumerate(resps) if r.status_code != 200]
    if not failed:
        return None
    total = len(addrs)
    ok = total - len(failed)
    lines = [f"PARTIAL DATA: {ok}/{total} workers responded"]
    for rank, resp in failed:
        lines.append(f"  Rank {rank}: {resp.text}")
    return "\n".join(lines)

