
def get_project_id():
    """Gets the project ID for the current App Engine application.

    Returns:
        str: The project ID

    Raises:
        google.auth.exceptions.OSError: If the App Engine APIs are unavailable.
    """
    # pylint: disable=missing-raises-doc
    # Pylint rightfully thinks google.auth.exceptions.OSError is OSError, but doesn't
    # realize it's a valid alias.
    if app_identity is None:
        raise exceptions.OSError("The App Engine APIs are not available.")
    return app_identity.get_application_id()


def get_project_id():
    """Gets the project ID from the Cloud SDK.

    Returns:
        Optional[str]: The project ID.
    """
    if os.name == "nt":
        command = _CLOUD_SDK_WINDOWS_COMMAND
    else:
        command = _CLOUD_SDK_POSIX_COMMAND

    try:
        # Ignore the stderr coming from gcloud, so it won't be mixed into the output.
        # https://github.com/googleapis/google-auth-library-python/issues/673
        project = _run_subprocess_ignore_stderr(
            (command,) + _CLOUD_SDK_CONFIG_GET_PROJECT_COMMAND
        )

        # Turn bytes into a string and remove "\n"
        project = _helpers.from_bytes(project).strip()
        return project if project else None
    except (subprocess.CalledProcessError, OSError, IOError):
        return None


def get_project_id(request):
    """Get the Google Cloud Project ID from the metadata server.

    Args:
        request (google.auth.transport.Request): A callable used to make
            HTTP requests.

    Returns:
        str: The project ID

    Raises:
        google.auth.exceptions.TransportError: if an error occurred while
            retrieving metadata.
    """
    return get(request, "project/project-id")

