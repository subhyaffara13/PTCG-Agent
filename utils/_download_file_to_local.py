
def _download_file_to_local(api: HfApi, src: str, dst: str | None) -> None:
    uri = parse_hf_uri(src)
    filename = _source_filename(uri, src)

    if dst is None:
        local_path = filename
    elif os.path.isdir(dst) or dst.endswith(os.sep) or dst.endswith("/"):
        local_path = os.path.join(dst, filename)
    else:
        local_path = dst

    parent_dir = os.path.dirname(local_path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    _download_single(api, uri, local_path)
    out.result("Downloaded", src=src, dst=local_path)

