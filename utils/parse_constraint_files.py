
def parse_constraint_files(
    constraint_files: list[str],
    finder: PackageFinder,
    options: Values,
    session: PipSession,
) -> list[InstallRequirement]:
    requirements = []
    for filename in constraint_files:
        for parsed_req in parse_requirements(
            filename,
            constraint=True,
            finder=finder,
            options=options,
            session=session,
        ):
            req_to_add = install_req_from_parsed_requirement(
                parsed_req,
                isolated=options.isolated_mode,
                user_supplied=False,
            )
            requirements.append(req_to_add)

    return requirements

