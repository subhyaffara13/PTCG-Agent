
def normalize_storage_type(storage_type):
    return getattr(torch, storage_type.__name__)

