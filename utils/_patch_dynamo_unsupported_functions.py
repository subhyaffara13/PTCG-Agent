
def _patch_dynamo_unsupported_functions():
    """Patch PyTorch to bypass some functions torch.export.export does not support."""
    # TODO: Remove the patches once dynamo supports these functions.
    import torch.jit

    # Replace torch.jit.isinstance with isinstance
    jit_isinstance = torch.jit.isinstance
    # pyrefly: ignore [bad-assignment]
    torch.jit.isinstance = isinstance
    logger.info("Replaced torch.jit.isinstance with isinstance to allow dynamo tracing")
    try:
        yield
    finally:
        torch.jit.isinstance = jit_isinstance

