
def get_dataloader_sampler(dataloader):
    if hasattr(dataloader, "batch_sampler") and dataloader.batch_sampler is not None:
        return get_dataloader_sampler(dataloader.batch_sampler)
    elif hasattr(dataloader, "sampler"):
        return dataloader.sampler

