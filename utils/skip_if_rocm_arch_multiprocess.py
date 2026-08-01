
def skip_if_rocm_arch_multiprocess(arch: tuple[str, ...]):
    """Skips a test for given ROCm archs - multiprocess UTs"""

    def decorator(func):
        reason = None
        if TEST_WITH_ROCM:
            prop = torch.cuda.get_device_properties(0).gcnArchName.split(":")[0]
            if prop in arch:
                reason = f"skip_if_rocm_arch_multiprocess: test skipped on {arch}"

        return unittest.skipIf(reason is not None, reason)(func)

    return decorator

