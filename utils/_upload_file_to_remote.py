import os
import sys

def _upload_file_to_remote(api: HfApi, src: str, dst: str, *, src_is_stdin: bool) -> None:
    uri = parse_hf_uri(dst)

    if src_is_stdin:
        if uri.path_in_repo == "" or dst.endswith("/"):
            raise typer.BadParameter("Stdin upload requires a full destination path including filename.")
        data = sys.stdin.buffer.read()
        _upload_single(api, uri, data, uri.path_in_repo)
        out.result("Uploaded", src="stdin", dst=uri.to_uri())
        return

    if os.path.isdir(src):
        raise typer.BadParameter(
            "Source must be a file, not a directory. Use `hf upload` or `hf buckets sync` for directories."
        )
    if not os.path.isfile(src):
        raise typer.BadParameter(f"Source file not found: {src}")

    prefix = uri.path_in_repo
    if prefix == "":
        remote_path = os.path.basename(src)
    elif dst.endswith("/"):
        remote_path = prefix + "/" + os.path.basename(src)
    else:
        remote_path = prefix

    _upload_single(api, uri, src, remote_path)
    out.result("Uploaded", src=src, dst=replace(uri, path_in_repo=remote_path).to_uri())

