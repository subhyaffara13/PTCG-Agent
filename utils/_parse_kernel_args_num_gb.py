import re

def _parse_kernel_args_num_gb(
    kernel_fn_code: str, kernel_category: str
) -> float | None:
    """
    inductor meta looks like:
        inductor_meta={... 'mutated_arg_names': [], 'no_x_dim': False, 'kernel_num_gb': 2.0},
    """
    m = re.search(r".kernel_num_gb.:\s*([0-9.]+)", kernel_fn_code)
    if m:
        return float(m.group(1))
    else:
        """
        There are a few cases that kernel_num_gdb field can be missing:
        1. the field will be missing if config.benchmark_kernel and
           config.profile_bandwidth are false
        2. even if config.benchmark_kernel or config.profile_bandwidth is true.
           foreach kernel does not have kernel_num_gb field in the metadata
        """
        return None

