
def FixtureRequest_fspath(self: FixtureRequest) -> LEGACY_PATH:
    """(deprecated) The file system path of the test module which collected this test."""
    return legacy_path(self.path)

