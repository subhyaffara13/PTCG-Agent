
def build_conda_download_url(purl):
    """
    Resolve a Conda PURL to a real downloadable URL

    Supported qualifiers:
      - channel: e.g., main, conda-forge (required for deterministic base)
      - subdir: e.g., linux-64, osx-arm64, win-64, noarch
      - build:  exact build string (optional but recommended)
      - type:   'conda' or 'tar.bz2' (preference; fallback to whichever exists)
    """
    p = PackageURL.from_string(purl)
    if not p.name or not p.version:
        return None

    q = p.qualifiers or {}
    name = p.name
    version = p.version
    build = q.get("build")
    channel = q.get("channel") or "main"
    subdir = q.get("subdir") or "noarch"
    req_type = q.get("type")

    def _conda_base_for_channel(channel: str) -> str:
        """
        Map a conda channel to its base URL.
        - 'main' / 'defaults' -> repo.anaconda.com
        - any other channel    -> conda.anaconda.org/<channel>
        """
        ch = (channel or "").lower()
        if ch in ("main", "defaults"):
            return "https://repo.anaconda.com/pkgs/main"
        return f"https://conda.anaconda.org/{ch}"

    base = _conda_base_for_channel(channel)

    package_identifier = (
        f"{name}-{version}-{build}.{req_type}" if build else f"{name}-{version}.{req_type}"
    )

    download_url = f"{base}/{subdir}/{package_identifier}"
    return download_url

