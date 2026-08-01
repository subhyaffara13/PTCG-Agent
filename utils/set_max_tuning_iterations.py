
def set_max_tuning_iterations(iterations: int) -> None:
    r"""Set max number of iterations to spend tuning a given solution.

    If both max tuning duration and iterations are set, the smaller of the two
    will be honored. At minimum 1 tuning iteration will always be run.
    """
    torch._C._cuda_tunableop_set_max_tuning_iterations(iterations)  # type: ignore[attr-defined]

