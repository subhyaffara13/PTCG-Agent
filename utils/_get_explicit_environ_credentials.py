import os

def _get_explicit_environ_credentials(quota_project_id=None):
    """Gets credentials from the GOOGLE_APPLICATION_CREDENTIALS environment
    variable."""
    from google.auth import _cloud_sdk

    cloud_sdk_adc_path = _cloud_sdk.get_application_default_credentials_path()
    explicit_file = os.environ.get(environment_vars.CREDENTIALS, "")

    _LOGGER.debug(
        "Checking '%s' for explicit credentials as part of auth process...",
        explicit_file,
    )

    if explicit_file != "" and explicit_file == cloud_sdk_adc_path:
        # Cloud sdk flow calls gcloud to fetch project id, so if the explicit
        # file path is cloud sdk credentials path, then we should fall back
        # to cloud sdk flow, otherwise project id cannot be obtained.
        _LOGGER.debug(
            "Explicit credentials path '%s' is the same as Cloud SDK credentials path, fall back to Cloud SDK credentials flow...",
            explicit_file,
        )
        return _get_gcloud_sdk_credentials(quota_project_id=quota_project_id)

    if explicit_file != "":
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            credentials, project_id = load_credentials_from_file(
                os.environ[environment_vars.CREDENTIALS],
                quota_project_id=quota_project_id,
            )
            credentials._cred_file_path = f"{explicit_file} file via the GOOGLE_APPLICATION_CREDENTIALS environment variable"
            return credentials, project_id

    else:
        return None, None


def _get_explicit_environ_credentials(quota_project_id=None):
    """Gets credentials from the GOOGLE_APPLICATION_CREDENTIALS environment
    variable."""
    from google.auth import _cloud_sdk

    cloud_sdk_adc_path = _cloud_sdk.get_application_default_credentials_path()
    explicit_file = os.environ.get(environment_vars.CREDENTIALS)

    if explicit_file is not None and explicit_file == cloud_sdk_adc_path:
        # Cloud sdk flow calls gcloud to fetch project id, so if the explicit
        # file path is cloud sdk credentials path, then we should fall back
        # to cloud sdk flow, otherwise project id cannot be obtained.
        return _get_gcloud_sdk_credentials(quota_project_id=quota_project_id)

    if explicit_file is not None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            credentials, project_id = load_credentials_from_file(
                os.environ[environment_vars.CREDENTIALS],
                quota_project_id=quota_project_id,
            )

            return credentials, project_id

    else:
        return None, None

