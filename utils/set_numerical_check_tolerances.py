
def set_numerical_check_tolerances(
    enable: bool, atol: float = 1e-5, rtol: float = 1e-5
) -> None:
    r"""Set the atol and rtol values in numeric check"""
    return torch._C._cuda_tunableop_set_numerical_check_tolerances(enable, atol, rtol)  # type: ignore[attr-defined]

