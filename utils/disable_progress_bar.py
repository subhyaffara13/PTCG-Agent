
def disable_progress_bar():
    """Disable tqdm progress bar."""
    global _tqdm_active
    _tqdm_active = False
    hf_hub_utils.disable_progress_bars()

