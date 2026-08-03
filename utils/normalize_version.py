from typing import Optional, Union

def normalize_version(
    version: AnyStr | None, ptype: Optional[Union[str, bytes]], encode: bool | None = True
) -> str | None:
    if not version:
        return None

    version_str = version if isinstance(version, str) else version.decode("utf-8")
    quoter = get_quoter(encode)
    version_str = quoter(version_str.strip())
    if ptype and isinstance(ptype, str) and ptype in ("huggingface", "oci"):
        return version_str.lower()
    return version_str or None


def normalize_version(version: str) -> str:
    """
    Remove the epoch (if any) from a Debian version.
    E.g., "1:2.4.47-2" becomes "2.4.47-2"
    """
    if ":" in version:
        _, v = version.split(":", 1)
        return v
    return version

