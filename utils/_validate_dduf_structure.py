from typing import Any

def _validate_dduf_structure(index: Any, entry_names: Iterable[str]) -> None:
    """
    Consistency checks on the DDUF file structure.

    Rules:
    - The 'model_index.json' entry is required and must contain a dictionary.
    - Each folder name must correspond to an entry in 'model_index.json'.
    - Each folder must contain at least a config file ('config.json', 'tokenizer_config.json', 'preprocessor_config.json', 'scheduler_config.json').

    Args:
        index (Any):
            The content of the 'model_index.json' entry.
        entry_names (Iterable[str]):
            The list of entry names in the DDUF file.

    Raises:
        - [`DDUFCorruptedFileError`]: If the DDUF file is corrupted (i.e. doesn't follow the DDUF format).
    """
    if not isinstance(index, dict):
        raise DDUFCorruptedFileError(f"Invalid 'model_index.json' content. Must be a dictionary. Got {type(index)}.")

    dduf_folders = {entry.split("/")[0] for entry in entry_names if "/" in entry}
    for folder in dduf_folders:
        if folder not in index:
            raise DDUFCorruptedFileError(f"Missing required entry '{folder}' in 'model_index.json'.")
        if not any(f"{folder}/{required_entry}" in entry_names for required_entry in DDUF_FOLDER_REQUIRED_ENTRIES):
            raise DDUFCorruptedFileError(
                f"Missing required file in folder '{folder}'. Must contains at least one of {DDUF_FOLDER_REQUIRED_ENTRIES}."
            )

