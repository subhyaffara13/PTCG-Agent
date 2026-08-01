
def _run_cp(src: str, dst: str | None, token: str | None) -> None:
    api = get_hf_api(token=token)

    src_is_stdin = src == "-"
    dst_is_stdout = dst == "-"
    src_is_hf = is_hf_uri(src)
    dst_is_hf = dst is not None and is_hf_uri(dst)

    # --- Remote to remote: delegate to copy_files (repo/bucket -> repo/bucket) ---
    if src_is_hf and dst_is_hf:
        assert dst is not None  # guaranteed by dst_is_hf
        api.copy_files(src, dst)
        out.result("Copied", src=src, dst=dst)
        return

    # --- At least one side must be a remote hf:// URI (rules out local->local, stdin->local, etc.) ---
    if not src_is_hf and not dst_is_hf:
        if dst is None:
            raise typer.BadParameter("Missing destination. Provide a repo or bucket hf:// URI as DST.")
        raise typer.BadParameter(
            "One of SRC or DST must be a repo (hf://username/...) or bucket (hf://buckets/...) URI."
        )

    # --- Download: repo/bucket -> local file or stdout ---
    if src_is_hf:
        if dst_is_stdout:
            _download_file_to_stdout(api, src)
            return
        _download_file_to_local(api, src, dst)
        return

    # --- Upload: local file or stdin -> repo/bucket ---
    assert dst is not None  # guaranteed: reaching here means dst_is_hf is True
    _upload_file_to_remote(api, src, dst, src_is_stdin=src_is_stdin)

