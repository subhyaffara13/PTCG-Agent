
def _validate_requirements(
    requirements: list[InstallRequirement],
) -> Generator[tuple[str, InstallRequirement], None, None]:
    for req in requirements:
        assert req.name, f"invalid to-be-installed requirement: {req}"
        yield req.name, req

