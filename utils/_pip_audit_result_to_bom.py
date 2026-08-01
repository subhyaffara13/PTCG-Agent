
def _pip_audit_result_to_bom(
    result: dict[service.Dependency, list[service.VulnerabilityResult]],
) -> Bom:
    vulnerabilities = []
    components = []

    for dep, vulns in result.items():
        # TODO(alex): Is there anything interesting we can do with skipped dependencies in
        # the CycloneDX format?
        if dep.is_skipped():
            continue
        dep = cast(service.ResolvedDependency, dep)

        c = Component(name=dep.name, version=str(dep.version))
        vuln_list = [
            Vulnerability(
                id=vuln.id,
                description=vuln.description,
                recommendation="Upgrade",
                # BomTarget expects str in type hints, but accepts BomRef at runtime
                affects=[BomTarget(ref=c.bom_ref)],  # type: ignore[arg-type]
            )
            for vuln in vulns
        ]
        vulnerabilities.extend(vuln_list)
        components.append(c)

    return Bom(components=components, vulnerabilities=vulnerabilities)

