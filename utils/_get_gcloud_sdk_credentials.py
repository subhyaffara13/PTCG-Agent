import os

def _get_gcloud_sdk_credentials(quota_project_id=None):
    """Gets the credentials and project ID from the Cloud SDK."""
    from google.auth import _cloud_sdk

    _LOGGER.debug("Checking Cloud SDK credentials as part of auth process...")

    # Check if application default credentials exist.
    credentials_filename = _cloud_sdk.get_application_default_credentials_path()

    if not os.path.isfile(credentials_filename):
        _LOGGER.debug("Cloud SDK credentials not found on disk; not using them")
        return None, None

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        credentials, project_id = load_credentials_from_file(
            credentials_filename, quota_project_id=quota_project_id
        )
        credentials._cred_file_path = credentials_filename

        if not project_id:
            project_id = _cloud_sdk.get_project_id()

        return credentials, project_id


def _get_gcloud_sdk_credentials(quota_project_id=None):
    """Gets the credentials and project ID from the Cloud SDK."""
    from google.auth import _cloud_sdk

    # Check if application default credentials exist.
    credentials_filename = _cloud_sdk.get_application_default_credentials_path()

    if not os.path.isfile(credentials_filename):
        return None, None

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        credentials, project_id = load_credentials_from_file(
            credentials_filename, quota_project_id=quota_project_id
        )

        if not project_id:
            project_id = _cloud_sdk.get_project_id()

        return credentials, project_id

