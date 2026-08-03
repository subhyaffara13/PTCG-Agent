import os
from pathlib import Path


def _compute_local_source_files_hash(
    pretrained_model_name_or_path: str | os.PathLike,
    resolved_module_file: str | os.PathLike,
) -> str:
    """
    Computes a stable hash from the bytes of the local source file and its relative-import source files.
    """
    model_path = Path(pretrained_model_name_or_path).resolve()
    resolved_module_file = Path(resolved_module_file).resolve()

    def _resolve_relative_source_path(source_file_path: Path) -> str:
        try:
            return source_file_path.relative_to(model_path).as_posix()
        except ValueError:
            # Fallback for edge cases where the source file is not under the local model directory.
            return source_file_path.as_posix()

    files_to_hash = [
        (_resolve_relative_source_path(resolved_module_file), resolved_module_file),
    ]
    for source_file in get_relative_import_files(resolved_module_file):
        source_file_path = Path(source_file).resolve()
        files_to_hash.append((_resolve_relative_source_path(source_file_path), source_file_path))

    source_files_hash = hashlib.sha256()
    for relative_path, file_path in sorted(files_to_hash, key=lambda entry: entry[0]):
        source_files_hash.update(relative_path.encode("utf-8"))
        source_files_hash.update(file_path.read_bytes())

    return source_files_hash.hexdigest()[:16]

