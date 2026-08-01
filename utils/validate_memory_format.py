
def validate_memory_format(memory_format: torch.memory_format):
    torch._check(
        memory_format in _memory_formats,
        lambda: f"Received unknown memory format {memory_format}!",
    )

