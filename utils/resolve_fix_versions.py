
def resolve_fix_versions(
    service: VulnerabilityService,
    result: dict[Dependency, list[VulnerabilityResult]],
    state: AuditState = AuditState(),
) -> Iterator[FixVersion]:
    """
    Resolves a mapping of dependencies to known vulnerabilities to a series of fix versions without
    known vulnerabilities.
    """
    for dep, vulns in result.items():
        if dep.is_skipped():
            continue
        if not vulns:
            continue
        dep = cast(ResolvedDependency, dep)
        try:
            version = _resolve_fix_version(service, dep, vulns, state)
            yield ResolvedFixVersion(dep, version)
        except FixResolutionImpossible as fri:
            skip_reason = str(fri)
            logger.debug(skip_reason)
            yield SkippedFixVersion(dep, skip_reason)

