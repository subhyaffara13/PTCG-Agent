import json
import os
from pathlib import Path


def export_entries_as_dduf(dduf_path: str | os.PathLike, entries: Iterable[tuple[str, str | Path | bytes]]) -> None:
    """Write a DDUF file from an iterable of entries.

    This is a lower-level helper than [`export_folder_as_dduf`] that allows more flexibility when serializing data.
    In particular, you don't need to save the data on disk before exporting it in the DDUF file.

    Args:
        dduf_path (`str` or `os.PathLike`):
            The path to the DDUF file to write.
        entries (`Iterable[tuple[str, Union[str, Path, bytes]]]`):
            An iterable of entries to write in the DDUF file. Each entry is a tuple with the filename and the content.
            The filename should be the path to the file in the DDUF archive.
            The content can be a string or a pathlib.Path representing a path to a file on the local disk or directly the content as bytes.

    Raises:
        - [`DDUFExportError`]: If anything goes wrong during the export (e.g. invalid entry name, missing 'model_index.json', etc.).

    Example:
        ```python
        # Export specific files from the local disk.
        >>> from huggingface_hub import export_entries_as_dduf
        >>> export_entries_as_dduf(
        ...     dduf_path="stable-diffusion-v1-4-FP16.dduf",
        ...     entries=[ # List entries to add to the DDUF file (here, only FP16 weights)
        ...         ("model_index.json", "path/to/model_index.json"),
        ...         ("vae/config.json", "path/to/vae/config.json"),
        ...         ("vae/diffusion_pytorch_model.fp16.safetensors", "path/to/vae/diffusion_pytorch_model.fp16.safetensors"),
        ...         ("text_encoder/config.json", "path/to/text_encoder/config.json"),
        ...         ("text_encoder/model.fp16.safetensors", "path/to/text_encoder/model.fp16.safetensors"),
        ...         # ... add more entries here
        ...     ]
        ... )
        ```

        ```python
        # Export state_dicts one by one from a loaded pipeline
        >>> from diffusers import DiffusionPipeline
        >>> from typing import Generator, Tuple
        >>> import safetensors.torch
        >>> from huggingface_hub import export_entries_as_dduf
        >>> pipe = DiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
        ... # ... do some work with the pipeline

        >>> def as_entries(pipe: DiffusionPipeline) -> Generator[tuple[str, bytes], None, None]:
        ...     # Build a generator that yields the entries to add to the DDUF file.
        ...     # The first element of the tuple is the filename in the DDUF archive (must use UNIX separator!). The second element is the content of the file.
        ...     # Entries will be evaluated lazily when the DDUF file is created (only 1 entry is loaded in memory at a time)
        ...     yield "vae/config.json", pipe.vae.to_json_string().encode()
        ...     yield "vae/diffusion_pytorch_model.safetensors", safetensors.torch.save(pipe.vae.state_dict())
        ...     yield "text_encoder/config.json", pipe.text_encoder.config.to_json_string().encode()
        ...     yield "text_encoder/model.safetensors", safetensors.torch.save(pipe.text_encoder.state_dict())
        ...     # ... add more entries here

        >>> export_entries_as_dduf(dduf_path="stable-diffusion-v1-4.dduf", entries=as_entries(pipe))
        ```
    """
    logger.info(f"Exporting DDUF file '{dduf_path}'")
    filenames = set()
    index = None
    with zipfile.ZipFile(str(dduf_path), "w", zipfile.ZIP_STORED) as archive:
        for filename, content in entries:
            if filename in filenames:
                raise DDUFExportError(f"Can't add duplicate entry: {filename}")
            filenames.add(filename)

            if filename == "model_index.json":
                try:
                    index = json.loads(_load_content(content).decode())
                except json.JSONDecodeError as e:
                    raise DDUFExportError("Failed to parse 'model_index.json'.") from e

            try:
                filename = _validate_dduf_entry_name(filename)
            except DDUFInvalidEntryNameError as e:
                raise DDUFExportError(f"Invalid entry name: {filename}") from e
            logger.debug(f"Adding entry '{filename}' to DDUF file")
            _dump_content_in_archive(archive, filename, content)

    # Consistency checks on the DDUF file
    if index is None:
        raise DDUFExportError("Missing required 'model_index.json' entry in DDUF file.")
    try:
        _validate_dduf_structure(index, filenames)
    except DDUFCorruptedFileError as e:
        raise DDUFExportError("Invalid DDUF file structure.") from e

    logger.info(f"Done writing DDUF file {dduf_path}")

