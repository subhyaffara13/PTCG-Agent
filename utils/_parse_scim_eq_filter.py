
def _parse_scim_eq_filter(scim_filter: str) -> Optional[Tuple[str, str]]:
    """Parse the SCIM equality filters Okta uses before user lifecycle changes."""
    match = re.match(
        r"""\s*([\w.]+)\s+eq\s+(['"]?)(.*?)\2\s*$""",
        scim_filter,
        flags=re.IGNORECASE,
    )
    if not match:
        return None
    return match.group(1).lower(), match.group(3)

