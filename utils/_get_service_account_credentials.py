
def _get_service_account_credentials(filename, info, scopes=None, default_scopes=None):
    from google.oauth2 import service_account

    try:
        credentials = service_account.Credentials.from_service_account_info(
            info, scopes=scopes, default_scopes=default_scopes
        )
    except ValueError as caught_exc:
        msg = "Failed to load service account credentials from {}".format(filename)
        new_exc = exceptions.DefaultCredentialsError(msg, caught_exc)
        raise new_exc from caught_exc
    return credentials, info.get("project_id")

