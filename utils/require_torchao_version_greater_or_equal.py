
def require_torchao_version_greater_or_equal(torchao_version):
    def decorator(test_case):
        correct_torchao_version = is_torchao_available() and version.parse(
            version.parse(importlib.metadata.version("torchao")).base_version
        ) >= version.parse(torchao_version)
        return unittest.skipUnless(
            correct_torchao_version, f"Test requires torchao with the version greater than {torchao_version}."
        )(test_case)

    return decorator

