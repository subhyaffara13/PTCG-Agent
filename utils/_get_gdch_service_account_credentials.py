
def _get_gdch_service_account_credentials(filename, info):
    from google.oauth2 import gdch_credentials

    try:
        credentials = (
            gdch_credentials.ServiceAccountCredentials.from_service_account_info(info)
        )
    except ValueError as caught_exc:
        msg = "Failed to load GDCH service account credentials from {}".format(filename)
        new_exc = exceptions.DefaultCredentialsError(msg, caught_exc)
        raise new_exc from caught_exc
    return credentials, info.get("project")

