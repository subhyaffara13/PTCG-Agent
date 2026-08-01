
def _format_csv(headers: list[str], rows: list[list[str]]) -> str:
    """Format data as CSV. Human-readable and easily parseable."""
    lines = [",".join(headers)]
    for row in rows:
        lines.append(",".join(str(v) for v in row))
    return "\n".join(lines)

