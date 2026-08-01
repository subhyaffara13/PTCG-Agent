
def pylock_from_install_requirements(
    install_requirements: Iterable[InstallRequirement], base_dir: Path
) -> Pylock:
    return Pylock(
        lock_version=Version("1.0"),
        created_by="pip",
        packages=sorted(
            (
                _pylock_package_from_install_requirement(ireq, base_dir)
                for ireq in install_requirements
            ),
            key=lambda p: p.name,
        ),
    )

