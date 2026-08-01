
def _source_filename(uri: HfUri, src: str) -> str:
    if uri.path_in_repo == "" or src.endswith("/"):
        raise typer.BadParameter(
            "Source path must include a file name, not just a repo/bucket or directory path."
            " Use `hf download` or `hf buckets sync` to copy directories."
        )
    return uri.path_in_repo.rsplit("/", 1)[-1]

