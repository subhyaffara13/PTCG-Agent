
def _append_sycl_std_if_no_std_present(cflags) -> None:
    if not any(flag.startswith('-sycl-std=') for flag in cflags):
        cflags.append('-sycl-std=2020')

