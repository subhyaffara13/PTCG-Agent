import json
import os

def load_credentials_from_file(
    filename, scopes=None, default_scopes=None, quota_project_id=None, request=None
):
    """Loads Google credentials from a file.

    The credentials file must be a service account key, stored authorized
    user credentials, external account credentials, or impersonated service
    account credentials.

    .. warning::
        Important: If you accept a credential configuration (credential JSON/File/Stream)
        from an external source for authentication to Google Cloud Platform, you must
        validate it before providing it to any Google API or client library. Providing an
        unvalidated credential configuration to Google APIs or libraries can compromise
        the security of your systems and data. For more information, refer to
        `Validate credential configurations from external sources`_.

        .. _Validate credential configurations from external sources:
            https://cloud.google.com/docs/authentication/external/externally-sourced-credentials

    Args:
        filename (str): The full path to the credentials file.
        scopes (Optional[Sequence[str]]): The list of scopes for the credentials. If
            specified, the credentials will automatically be scoped if
            necessary
        default_scopes (Optional[Sequence[str]]): Default scopes passed by a
            Google client library. Use 'scopes' for user-defined scopes.
        quota_project_id (Optional[str]):  The project ID used for
            quota and billing.
        request (Optional[google.auth.transport.Request]): An object used to make
            HTTP requests. This is used to determine the associated project ID
            for a workload identity pool resource (external account credentials).
            If not specified, then it will use a
            google.auth.transport.requests.Request client to make requests.

    Returns:
        Tuple[google.auth.credentials.Credentials, Optional[str]]: Loaded
            credentials and the project ID. Authorized user credentials do not
            have the project ID information. External account credentials project
            IDs may not always be determined.

    Raises:
        google.auth.exceptions.DefaultCredentialsError: if the file is in the
            wrong format or is missing.
    """
    _warn_about_generic_load_method("load_credentials_from_file")

    if not os.path.exists(filename):
        raise exceptions.DefaultCredentialsError(
            "File {} was not found.".format(filename)
        )

    with io.open(filename, "r") as file_obj:
        try:
            info = json.load(file_obj)
        except ValueError as caught_exc:
            new_exc = exceptions.DefaultCredentialsError(
                "File {} is not a valid json file.".format(filename), caught_exc
            )
            raise new_exc from caught_exc
    return _load_credentials_from_info(
        filename, info, scopes, default_scopes, quota_project_id, request
    )


def load_credentials_from_file(filename, scopes=None, quota_project_id=None):
    """Loads Google credentials from a file.

    The credentials file must be a service account key or stored authorized
    user credentials.

    Args:
        filename (str): The full path to the credentials file.
        scopes (Optional[Sequence[str]]): The list of scopes for the credentials. If
            specified, the credentials will automatically be scoped if
            necessary
        quota_project_id (Optional[str]):  The project ID used for
                quota and billing.

    Returns:
        Tuple[google.auth.credentials.Credentials, Optional[str]]: Loaded
            credentials and the project ID. Authorized user credentials do not
            have the project ID information.

    Raises:
        google.auth.exceptions.DefaultCredentialsError: if the file is in the
            wrong format or is missing.
    """
    if not os.path.exists(filename):
        raise exceptions.DefaultCredentialsError(
            "File {} was not found.".format(filename)
        )

    with io.open(filename, "r") as file_obj:
        try:
            info = json.load(file_obj)
        except ValueError as caught_exc:
            new_exc = exceptions.DefaultCredentialsError(
                "File {} is not a valid json file.".format(filename), caught_exc
            )
            raise new_exc from caught_exc

    # The type key should indicate that the file is either a service account
    # credentials file or an authorized user credentials file.
    credential_type = info.get("type")

    if credential_type == _default._AUTHORIZED_USER_TYPE:
        from google.oauth2 import _credentials_async as credentials

        try:
            credentials = credentials.Credentials.from_authorized_user_info(
                info, scopes=scopes
            )
        except ValueError as caught_exc:
            msg = "Failed to load authorized user credentials from {}".format(filename)
            new_exc = exceptions.DefaultCredentialsError(msg, caught_exc)
            raise new_exc from caught_exc
        if quota_project_id:
            credentials = credentials.with_quota_project(quota_project_id)
        if not credentials.quota_project_id:
            _default._warn_about_problematic_credentials(credentials)
        return credentials, None

    elif credential_type == _default._SERVICE_ACCOUNT_TYPE:
        from google.oauth2 import _service_account_async as service_account

        try:
            credentials = service_account.Credentials.from_service_account_info(
                info, scopes=scopes
            ).with_quota_project(quota_project_id)
        except ValueError as caught_exc:
            msg = "Failed to load service account credentials from {}".format(filename)
            new_exc = exceptions.DefaultCredentialsError(msg, caught_exc)
            raise new_exc from caught_exc
        return credentials, info.get("project_id")

    else:
        raise exceptions.DefaultCredentialsError(
            "The file {file} does not have a valid type. "
            "Type is {type}, expected one of {valid_types}.".format(
                file=filename, type=credential_type, valid_types=_default._VALID_TYPES
            )
        )

