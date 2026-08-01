
def list_credential_helpers(folder: str | None = None) -> list[str]:
    """Return the list of git credential helpers configured.

    See https://git-scm.com/docs/gitcredentials.

    Credentials are saved in all configured helpers (store, cache, macOS keychain,...).
    Calls "`git credential approve`" internally. See https://git-scm.com/docs/git-credential.

    Args:
        folder (`str`, *optional*):
            The folder in which to check the configured helpers.
    """
    try:
        output = run_subprocess("git config --list", folder=folder).stdout
        parsed = _parse_credential_output(output)
        return parsed
    except subprocess.CalledProcessError as exc:
        raise OSError(exc.stderr)

