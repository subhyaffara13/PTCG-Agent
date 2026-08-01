
def _get_external_account_authorized_user_credentials(
    filename, info, scopes=None, default_scopes=None, request=None
):
    try:
        from google.auth import external_account_authorized_user

        credentials = external_account_authorized_user.Credentials.from_info(info)
    except ValueError:
        raise exceptions.DefaultCredentialsError(
            "Failed to load external account authorized user credentials from {}".format(
                filename
            )
        )

    return credentials, None

