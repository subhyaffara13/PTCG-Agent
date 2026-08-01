
def _get_authorized_user_credentials(filename, info, scopes=None):
    from google.oauth2 import credentials

    try:
        credentials = credentials.Credentials.from_authorized_user_info(
            info, scopes=scopes
        )
    except ValueError as caught_exc:
        msg = "Failed to load authorized user credentials from {}".format(filename)
        new_exc = exceptions.DefaultCredentialsError(msg, caught_exc)
        raise new_exc from caught_exc
    return credentials, None

