
def read_file(path: str | Path, fallback: str | None = None) -> str:
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception:
        if fallback is not None:
            return fallback
        raise NotFound(f"{path} not found")


def read_file(blobpath: str) -> bytes:
    if "://" not in blobpath:
        with open(blobpath, "rb", buffering=0) as f:
            return f.read()

    if blobpath.startswith(("http://", "https://")):
        # avoiding blobfile for public files helps avoid auth issues, like MFA prompts.
        import requests

        resp = requests.get(blobpath)
        resp.raise_for_status()
        return resp.content

    try:
        import blobfile
    except ImportError as e:
        raise ImportError(
            "blobfile is not installed. Please install it by running `pip install blobfile`."
        ) from e
    return blobfile.read_bytes(blobpath)


def read_file(filename: str | None = None) -> bool:
    r"""Read results from a TunableOp CSV file.

    If :attr:`filename` is not given, ``get_filename()`` is called.
    """
    if filename is None:
        filename = get_filename()
    return torch._C._cuda_tunableop_read_file(filename)  # type: ignore[attr-defined]


def read_file(fname: Path | str) -> list[str]:
    with open(fname, encoding="utf-8") as f:
        return f.readlines()

