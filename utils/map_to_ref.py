
def map_to_ref(t: Tensor | None) -> StorageWeakRefWrapper | None:
    if not isinstance(t, torch.Tensor):
        assert t is None
        return None
    return StorageWeakRefWrapper(t)

