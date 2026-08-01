
def get_filename() -> str:
    r"""Get the results filename."""
    return torch._C._cuda_tunableop_get_filename()  # type: ignore[attr-defined]

