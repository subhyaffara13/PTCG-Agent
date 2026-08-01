
def check_version(version_by_ranks: dict[str, str], version: str) -> None:
    for rank, v in version_by_ranks.items():
        if v != version:
            raise AssertionError(
                f"Rank {rank} has different version {v} from the given version {version}"
            )


def check_version(module, min_ver):
    if type(module) is MissingModule:
        return pytest.mark.skip(reason=f"{module.name} is not installed")
    return pytest.mark.skipif(
        version.parse(module.__version__) < version.Version(min_ver),
        reason=f"{module.__name__} version >= {min_ver} required"
    )

