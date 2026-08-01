
def get_auth_access_token(account=None):
    """Load user access token with the ``gcloud auth print-access-token`` command.

    Args:
        account (Optional[str]): Account to get the access token for. If not
            specified, the current active account will be used.

    Returns:
        str: The user access token.

    Raises:
        google.auth.exceptions.UserAccessTokenError: if failed to get access
            token from gcloud.
    """
    if os.name == "nt":
        command = _CLOUD_SDK_WINDOWS_COMMAND
    else:
        command = _CLOUD_SDK_POSIX_COMMAND

    try:
        if account:
            command = (
                (command,)
                + _CLOUD_SDK_USER_ACCESS_TOKEN_COMMAND
                + ("--account=" + account,)
            )
        else:
            command = (command,) + _CLOUD_SDK_USER_ACCESS_TOKEN_COMMAND

        access_token = subprocess.check_output(command, stderr=subprocess.STDOUT)
        # remove the trailing "\n"
        return access_token.decode("utf-8").strip()
    except (subprocess.CalledProcessError, OSError, IOError) as caught_exc:
        new_exc = exceptions.UserAccessTokenError(
            "Failed to obtain access token", caught_exc
        )
        raise new_exc from caught_exc

