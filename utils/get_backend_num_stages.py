
def get_backend_num_stages() -> int:
    from .runtime.triton_helpers import get_backend_options

    options = get_backend_options()
    return options.get("num_stages", 2 if torch.version.hip else 3)

