
def _set_real_storage(
    base: torch.UntypedStorage, real_storage: torch.UntypedStorage
) -> None:
    base.real_storage = real_storage  # type: ignore[attr-defined]

