
def _append_domain_filters(query: str, domains: list[str]) -> str:
    domain_clauses = " OR ".join(f"site:{d}" for d in domains)
    return f"({query}) ({domain_clauses})"

