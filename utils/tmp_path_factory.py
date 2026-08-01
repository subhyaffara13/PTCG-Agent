
def tmp_path_factory(request: FixtureRequest) -> TempPathFactory:
    """Return a :class:`pytest.TempPathFactory` instance for the test session."""
    # Set dynamically by pytest_configure() above.
    return request.config._tmp_path_factory  # type: ignore

