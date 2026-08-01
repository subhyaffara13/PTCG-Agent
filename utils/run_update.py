
def run_update() -> int:
    """Run the install-method-appropriate update command for the `hf` CLI.

    Raises CLIError if the installation method can't be determined.
    Returns the subprocess exit code on success/failure of the update itself.
    """
    cmd = _get_huggingface_hub_update_command()
    if cmd is None:
        raise CLIError(
            "Cannot determine how to update huggingface_hub (unknown installation method). Please update manually."
        )
    return subprocess.call(cmd)

