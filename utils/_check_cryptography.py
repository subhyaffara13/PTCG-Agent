
def _check_cryptography(cryptography_version: str) -> None:
    # cryptography < 1.3.4
    try:
        cryptography_version_list = list(map(int, cryptography_version.split(".")))
    except ValueError:
        return

    if cryptography_version_list < [1, 3, 4]:
        warning = f"Old version of cryptography ({cryptography_version_list}) may cause slowdown."
        warnings.warn(warning, RequestsDependencyWarning)


def _check_cryptography(cryptography_version):
    # cryptography < 1.3.4
    try:
        cryptography_version = list(map(int, cryptography_version.split(".")))
    except ValueError:
        return

    if cryptography_version < [1, 3, 4]:
        warning = (
            f"Old version of cryptography ({cryptography_version}) may cause slowdown."
        )
        warnings.warn(warning, RequestsDependencyWarning)

