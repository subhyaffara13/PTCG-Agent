
def location_tag(
    storage: Storage | torch.storage.TypedStorage | torch.UntypedStorage,
):
    for _, tagger, _ in _package_registry:
        location = tagger(storage)
        if location:
            return location
    raise RuntimeError(
        "don't know how to determine data location of " + torch.typename(storage)
    )

