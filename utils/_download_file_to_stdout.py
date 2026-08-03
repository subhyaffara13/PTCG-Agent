import os
import sys

def _download_file_to_stdout(api: HfApi, src: str) -> None:
    uri = parse_hf_uri(src)
    filename = _source_filename(uri, src)
    # Suppress progress bars to avoid polluting the piped output.
    with disable_progress_bars():
        with SoftTemporaryDirectory() as tmp_dir:
            tmp_path = os.path.join(tmp_dir, filename)
            _download_single(api, uri, tmp_path)
            with open(tmp_path, "rb") as f:
                while chunk := f.read(32_000_000):  # 32MB chunks
                    sys.stdout.buffer.write(chunk)

