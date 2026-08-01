
def get_cuda_version() -> str | None:
    try:
        cuda_version = config.cuda.version
        if cuda_version is None:
            cuda_version = torch.version.cuda
        return cuda_version
    except Exception:
        log.exception("Error getting cuda version")
        return None

