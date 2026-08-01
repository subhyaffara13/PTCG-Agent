
def enable_progress_bar():
    """Enable tqdm progress bar."""
    global _tqdm_active
    _tqdm_active = True
    hf_hub_utils.enable_progress_bars()

