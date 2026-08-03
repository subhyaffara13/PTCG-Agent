import os
from pathlib import Path


def export_folder_as_dduf(dduf_path: str | os.PathLike, folder_path: str | os.PathLike) -> None:
    """
    Export a folder as a DDUF file.

    AUses [`export_entries_as_dduf`] under the hood.

    Args:
        dduf_path (`str` or `os.PathLike`):
            The path to the DDUF file to write.
        folder_path (`str` or `os.PathLike`):
            The path to the folder containing the diffusion model.

    Example:
        ```python
        >>> from huggingface_hub import export_folder_as_dduf
        >>> export_folder_as_dduf(dduf_path="FLUX.1-dev.dduf", folder_path="path/to/FLUX.1-dev")
        ```
    """
    folder_path = Path(folder_path)

    def _iterate_over_folder() -> Iterable[tuple[str, Path]]:
        for path in Path(folder_path).glob("**/*"):
            if not path.is_file():
                continue
            if path.suffix not in DDUF_ALLOWED_ENTRIES:
                logger.debug(f"Skipping file '{path}' (file type not allowed)")
                continue
            path_in_archive = path.relative_to(folder_path)
            if len(path_in_archive.parts) >= 3:
                logger.debug(f"Skipping file '{path}' (nested directories not allowed)")
                continue
            yield path_in_archive.as_posix(), path

    export_entries_as_dduf(dduf_path, _iterate_over_folder())

