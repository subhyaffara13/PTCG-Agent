
def clean_memory() -> None:
    """Clean memory to avoid OOM."""
    gc.collect()
    torch.cuda.empty_cache()

