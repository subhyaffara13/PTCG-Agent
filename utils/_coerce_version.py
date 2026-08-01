
def _coerce_version(version: UnparsedVersion) -> Version | None:
    if not isinstance(version, Version):
        try:
            version = Version(version)
        except InvalidVersion:
            return None
    return version


def _coerce_version(version: UnparsedVersion) -> Version | None:
    if not isinstance(version, Version):
        try:
            version = Version(version)
        except InvalidVersion:
            return None
    return version


def _coerce_version(version: UnparsedVersion) -> Version | None:
    if not isinstance(version, Version):
        try:
            version = Version(version)
        except InvalidVersion:
            return None
    return version

