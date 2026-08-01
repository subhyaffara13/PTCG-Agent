
def _raise_on_head_call_error(head_call_error: Exception, force_download: bool, local_files_only: bool) -> NoReturn:
    """Raise an appropriate error when the HEAD call failed and we cannot locate a local file."""
    # No head call => we cannot force download.
    if force_download:
        if local_files_only:
            raise ValueError("Cannot pass 'force_download=True' and 'local_files_only=True' at the same time.")
        elif isinstance(head_call_error, OfflineModeIsEnabled):
            raise ValueError("Cannot pass 'force_download=True' when offline mode is enabled.") from head_call_error
        else:
            raise ValueError("Force download failed due to the above error.") from head_call_error

    # No head call + couldn't find an appropriate file on disk => raise an error.
    if local_files_only:
        raise LocalEntryNotFoundError(
            "Cannot find the requested files in the disk cache and outgoing traffic has been disabled. To enable"
            " hf.co look-ups and downloads online, set 'local_files_only' to False."
        )
    elif isinstance(head_call_error, (RepositoryNotFoundError, GatedRepoError)) or (
        isinstance(head_call_error, HfHubHTTPError) and head_call_error.response.status_code == 401
    ):
        # Repo not found or gated => let's raise the actual error
        # Unauthorized => likely a token issue => let's raise the actual error
        raise head_call_error
    else:
        # Otherwise: most likely a connection issue or Hub downtime => let's warn the user
        raise LocalEntryNotFoundError(
            "An error happened while trying to locate the file on the Hub and we cannot find the requested files"
            " in the local cache. Please check your connection and try again or make sure your Internet connection"
            " is on."
        ) from head_call_error

