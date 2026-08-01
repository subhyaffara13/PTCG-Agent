
def build_alpm_download_url(purl_str):
    purl = PackageURL.from_string(purl_str)
    name = purl.name
    version = purl.version
    arch = purl.qualifiers.get("arch", "any")

    if not name or not version:
        return None

    first_letter = name[0]
    url = f"https://archive.archlinux.org/packages/{first_letter}/{name}/{name}-{version}-{arch}.pkg.tar.zst"
    return url

