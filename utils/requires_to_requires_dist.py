
def requires_to_requires_dist(requirement: Requirement) -> str:
    """Return the version specifier for a requirement in PEP 345/566 fashion."""
    if requirement.url:
        return " @ " + requirement.url

    requires_dist: list[str] = []
    for spec in requirement.specifier:
        requires_dist.append(spec.operator + spec.version)

    if requires_dist:
        return " " + ",".join(sorted(requires_dist))
    else:
        return ""

