
def _get_real_storage(base: torch.UntypedStorage) -> torch.UntypedStorage:
    return base.real_storage  # type: ignore[attr-defined]

