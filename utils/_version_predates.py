
def _version_predates(lib: ModuleType, version: str) -> bool:
    """Helper function for checking version compatibility."""
    return Version(lib.__version__) < Version(version)

