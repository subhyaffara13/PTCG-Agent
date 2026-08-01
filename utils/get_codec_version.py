
def get_codec_version(codec_name: str) -> str | None:
    versions = _avif.codec_versions()
    for version in versions.split(", "):
        if version.split(" [")[0] == codec_name:
            return version.split(":")[-1].split(" ")[0]
    return None

