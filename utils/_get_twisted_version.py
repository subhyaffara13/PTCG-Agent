
def _get_twisted_version() -> TwistedVersion:
    # We need to check if "twisted.trial.unittest" is specifically present in sys.modules.
    # This is because we intend to integrate with Trial only when it's actively running
    # the test suite, but not needed when only other Twisted components are in use.
    if "twisted.trial.unittest" not in sys.modules:
        return TwistedVersion.NotInstalled

    import importlib.metadata

    import packaging.version

    version_str = importlib.metadata.version("twisted")
    version = packaging.version.parse(version_str)
    if version.major <= 24:
        return TwistedVersion.Version24
    else:
        return TwistedVersion.Version25

