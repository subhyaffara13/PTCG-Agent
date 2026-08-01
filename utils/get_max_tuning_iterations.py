
def get_max_tuning_iterations() -> int:
    r"""Get max iterations to spend tuning a given solution."""
    return torch._C._cuda_tunableop_get_max_tuning_iterations()  # type: ignore[attr-defined]

