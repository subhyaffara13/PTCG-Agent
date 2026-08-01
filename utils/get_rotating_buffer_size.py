
def get_rotating_buffer_size() -> int:
    r"""Get the rotating buffer size in kilobytes."""
    return torch._C._cuda_tunableop_get_rotating_buffer_size()  # type: ignore[attr-defined]

