
def _resolve_fix_version(
    service: VulnerabilityService,
    dep: ResolvedDependency,
    vulns: list[VulnerabilityResult],
    state: AuditState,
) -> Version:
    # We need to upgrade to a fix version that satisfies all vulnerability results
    #
    # However, whenever we upgrade a dependency, we run the risk of introducing new vulnerabilities
    # so we need to run this in a loop and continue polling the vulnerability service on each
    # prospective resolved fix version
    current_version = dep.version
    current_vulns = vulns
    while current_vulns:
        state.update_state(f"Resolving fix version for {dep.name}, checking {current_version}")

        def get_earliest_fix_version(d: ResolvedDependency, v: VulnerabilityResult) -> Version:
            for fix_version in v.fix_versions:
                if fix_version > current_version:
                    return fix_version
            raise FixResolutionImpossible(
                f"failed to fix dependency {dep.name} ({dep.version}), unable to find fix version "
                f"for vulnerability {v.id}"
            )

        # We want to retrieve a version that potentially fixes all vulnerabilities
        current_version = max([get_earliest_fix_version(dep, v) for v in current_vulns])
        _, current_vulns = service.query(ResolvedDependency(dep.name, current_version))
    return current_version

