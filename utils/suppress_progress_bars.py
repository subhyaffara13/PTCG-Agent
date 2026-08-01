
def suppress_progress_bars():
    """Context manager that suppresses huggingface_hub progress bars."""
    import huggingface_hub.utils as hf_hub_utils

    hf_hub_utils.disable_progress_bars()
    try:
        yield
    finally:
        hf_hub_utils.enable_progress_bars()

