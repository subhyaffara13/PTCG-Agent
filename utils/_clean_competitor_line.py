
def _clean_competitor_line(line: str) -> Optional[str]:
    """Strip numbering, bullets, and whitespace from a competitor name line."""
    name = line.strip().strip(".-) ").strip()
    return name if name and len(name) > 1 else None

