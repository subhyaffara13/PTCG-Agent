
def _meta_deserialize(obj, location):
    if location == "meta":
        return torch.UntypedStorage(obj.nbytes(), device="meta")

