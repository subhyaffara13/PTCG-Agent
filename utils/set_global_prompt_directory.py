
def set_global_prompt_directory(directory: str) -> None:
    """
    Set the global prompt directory for dotprompt files.

    Args:
        directory: Path to directory containing .prompt files
    """
    import litellm

    litellm.global_prompt_directory = directory  # type: ignore

