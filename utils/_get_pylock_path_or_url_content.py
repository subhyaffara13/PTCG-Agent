from pathlib import Path


def _get_pylock_path_or_url_content(path_or_url: str, session: PipSession) -> str:
    # TODO: refactor - this is similar to req_file.get_file_content
    scheme = urlsplit(path_or_url).scheme
    # Pip has special support for file:// URLs (LocalFSAdapter).
    if scheme in ["http", "https", "file"]:
        # Delay importing heavy network modules until absolutely necessary.
        from pip._internal.network.utils import raise_for_status

        resp = session.get(path_or_url)
        raise_for_status(resp)
        return resp.text

    # Assume this is a bare path.
    return Path(path_or_url).read_text(encoding="utf-8")

