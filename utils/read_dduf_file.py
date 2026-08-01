
def read_dduf_file(dduf_path: os.PathLike | str) -> dict[str, DDUFEntry]:
    """
    Read a DDUF file and return a dictionary of entries.

    Only the metadata is read, the data is not loaded in memory.

    Args:
        dduf_path (`str` or `os.PathLike`):
            The path to the DDUF file to read.

    Returns:
        `dict[str, DDUFEntry]`:
            A dictionary of [`DDUFEntry`] indexed by filename.

    Raises:
        - [`DDUFCorruptedFileError`]: If the DDUF file is corrupted (i.e. doesn't follow the DDUF format).

    Example:
        ```python
        >>> import json
        >>> import safetensors.torch
        >>> from huggingface_hub import read_dduf_file

        # Read DDUF metadata
        >>> dduf_entries = read_dduf_file("FLUX.1-dev.dduf")

        # Returns a mapping filename <> DDUFEntry
        >>> dduf_entries["model_index.json"]
        DDUFEntry(filename='model_index.json', offset=66, length=587)

        # Load model index as JSON
        >>> json.loads(dduf_entries["model_index.json"].read_text())
        {'_class_name': 'FluxPipeline', '_diffusers_version': '0.32.0.dev0', '_name_or_path': 'black-forest-labs/FLUX.1-dev', ...

        # Load VAE weights using safetensors
        >>> with dduf_entries["vae/diffusion_pytorch_model.safetensors"].as_mmap() as mm:
        ...     state_dict = safetensors.torch.load(mm)
        ```
    """
    entries = {}
    dduf_path = Path(dduf_path)
    logger.info(f"Reading DDUF file {dduf_path}")
    with zipfile.ZipFile(str(dduf_path), "r") as zf:
        for info in zf.infolist():
            logger.debug(f"Reading entry {info.filename}")
            if info.compress_type != zipfile.ZIP_STORED:
                raise DDUFCorruptedFileError("Data must not be compressed in DDUF file.")

            try:
                _validate_dduf_entry_name(info.filename)
            except DDUFInvalidEntryNameError as e:
                raise DDUFCorruptedFileError(f"Invalid entry name in DDUF file: {info.filename}") from e

            offset = _get_data_offset(zf, info)

            entries[info.filename] = DDUFEntry(
                filename=info.filename, offset=offset, length=info.file_size, dduf_path=dduf_path
            )

    # Consistency checks on the DDUF file
    if "model_index.json" not in entries:
        raise DDUFCorruptedFileError("Missing required 'model_index.json' entry in DDUF file.")
    index = json.loads(entries["model_index.json"].read_text())
    _validate_dduf_structure(index, entries.keys())

    logger.info(f"Done reading DDUF file {dduf_path}. Found {len(entries)} entries")
    return entries

