
def _get_impersonated_service_account_credentials(filename, info, scopes):
    from google.auth import impersonated_credentials

    try:
        credentials = (
            impersonated_credentials.Credentials.from_impersonated_service_account_info(
                info, scopes=scopes
            )
        )
    except ValueError as caught_exc:
        msg = "Failed to load impersonated service account credentials from {}".format(
            filename
        )
        new_exc = exceptions.DefaultCredentialsError(msg, caught_exc)
        raise new_exc from caught_exc
    return credentials, None

