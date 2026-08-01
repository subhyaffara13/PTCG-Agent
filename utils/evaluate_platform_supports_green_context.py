
def evaluate_platform_supports_green_context():
    if IS_WINDOWS:
        return False
    if not _get_torch_cuda_version() >= (12, 8):
        return False
    driver_version = torch.utils.collect_env.get_nvidia_driver_version(torch.utils.collect_env.run)
    if driver_version is None:
        return False
    return int(driver_version.split('.')[0]) >= 570

