
def _append_sycl_targets_if_missing(cflags) -> None:
    if any(flag.startswith('-fsycl-targets=') for flag in cflags):
        # do nothing: user has manually specified sycl targets
        return
    if _get_sycl_arch_list() != '':
        # AOT (spir64_gen) + JIT (spir64)
        cflags.append('-fsycl-targets=spir64_gen,spir64')
    else:
        # JIT (spir64)
        cflags.append('-fsycl-targets=spir64')

