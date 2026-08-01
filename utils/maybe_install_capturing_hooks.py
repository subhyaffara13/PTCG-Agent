
def maybe_install_capturing_hooks(model: PreTrainedModel) -> None:
    """
    Check if the model already has output capturing hooks installed, and install them if it is not already the
    case.
    Note that this is thread-safe, in case 2 (or more) threads want to install them concurrently.
    """
    # First check
    if getattr(model, "_output_capturing_hooks_installed", False):
        return

    with _hook_installation_lock:
        # Second check, in case several threads entered this function concurrently and did not return on the
        # previous check
        if getattr(model, "_output_capturing_hooks_installed", False):
            return
        # This will install the hooks and mark the model as hooked
        install_all_output_capturing_hooks(model)

