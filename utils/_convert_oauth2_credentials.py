
def _convert_oauth2_credentials(credentials):
    """Converts to :class:`google.oauth2.credentials.Credentials`.

    Args:
        credentials (Union[oauth2client.client.OAuth2Credentials,
            oauth2client.client.GoogleCredentials]): The credentials to
            convert.

    Returns:
        google.oauth2.credentials.Credentials: The converted credentials.
    """
    new_credentials = google.oauth2.credentials.Credentials(
        token=credentials.access_token,
        refresh_token=credentials.refresh_token,
        token_uri=credentials.token_uri,
        client_id=credentials.client_id,
        client_secret=credentials.client_secret,
        scopes=credentials.scopes,
    )

    new_credentials._expires = credentials.token_expiry

    return new_credentials

