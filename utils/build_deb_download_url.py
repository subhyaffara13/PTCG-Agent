
def build_deb_download_url(purl_str: str) -> str:
    """
    Construct a download URL for a Debian or Ubuntu package PURL.
    Supports optional 'repository_url' in qualifiers.
    """
    p = PackageURL.from_string(purl_str)

    name = p.name
    version = p.version
    namespace = p.namespace
    qualifiers = p.qualifiers or {}
    arch = qualifiers.get("arch")
    repository_url = qualifiers.get("repository_url")

    if not name or not version:
        raise ValueError("Both name and version must be present in deb purl")

    if not arch:
        arch = "source"

    if repository_url:
        base_url = repository_url.rstrip("/")
    else:
        if namespace == "debian":
            base_url = "https://deb.debian.org/debian"
        elif namespace == "ubuntu":
            base_url = "http://archive.ubuntu.com/ubuntu"
        else:
            raise NotImplementedError(f"Unsupported distro namespace: {namespace}")

    norm_version = normalize_version(version)

    if arch == "source":
        filename = f"{name}_{norm_version}.dsc"
    else:
        filename = f"{name}_{norm_version}_{arch}.deb"

    pool_path = f"/pool/main/{name[0].lower()}/{name}"

    return f"{base_url}{pool_path}/{filename}"

