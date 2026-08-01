
def urls_from_file(list_file: Path) -> list[str]:
    """``list_file`` should be a text file where each line corresponds to a URL to
    download.
    """
    print(f"file: {list_file}")
    content = list_file.read_text(encoding="utf-8")
    return [url for url in content.splitlines() if not url.startswith("#")]

