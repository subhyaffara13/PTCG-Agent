
def parallel_info() -> str:
    r"""Returns detailed string with parallelization settings"""
    return torch._C._parallel_info()

