
def get_all_device_types() -> list[str]:
    return ["cpu"] if not torch.cuda.is_available() else ["cpu", "cuda"]

