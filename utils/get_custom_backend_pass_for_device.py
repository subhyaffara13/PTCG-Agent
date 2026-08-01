
def get_custom_backend_pass_for_device(device: str) -> CustomGraphModulePass | None:
    return custom_backend_passes.get(device)

