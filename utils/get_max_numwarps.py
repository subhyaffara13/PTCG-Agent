
def get_max_numwarps() -> int:
    if torch.cuda.is_available():
        warp_size = torch.cuda.get_device_properties().warp_size
        # pyrefly: ignore [missing-attribute]
        max_threads_per_block = torch.cuda.get_device_properties().max_threads_per_block
    else:
        # Defaults
        warp_size = 32
        max_threads_per_block = 1024
    return max_threads_per_block // warp_size

