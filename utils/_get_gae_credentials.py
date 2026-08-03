import os

def _get_gae_credentials():
    """Gets Google App Engine App Identity credentials and project ID."""
    # If not GAE gen1, prefer the metadata service even if the GAE APIs are
    # available as per https://google.aip.dev/auth/4115.
    if os.environ.get(environment_vars.LEGACY_APPENGINE_RUNTIME) != "python27":
        return None, None

    # While this library is normally bundled with app_engine, there are
    # some cases where it's not available, so we tolerate ImportError.
    try:
        _LOGGER.debug("Checking for App Engine runtime as part of auth process...")
        import google.auth.app_engine as app_engine
    except ImportError:
        _LOGGER.warning("Import of App Engine auth library failed.")
        return None, None

    try:
        credentials = app_engine.Credentials()
        project_id = app_engine.get_project_id()
        return credentials, project_id
    except EnvironmentError:
        _LOGGER.debug(
            "No App Engine library was found so cannot authentication via App Engine Identity Credentials."
        )
        return None, None


def _get_gae_credentials():
    """Gets Google App Engine App Identity credentials and project ID."""
    # While this library is normally bundled with app_engine, there are
    # some cases where it's not available, so we tolerate ImportError.

    return _default._get_gae_credentials()

