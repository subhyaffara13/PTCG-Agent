
def get_file_extension(url: str) -> str:
    url = stringify_path(url)
    ext_parts = url.rsplit(".", 1)
    if len(ext_parts) > 1:
        return ext_parts[-1]
    return ""

