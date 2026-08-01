
def skipCUDAIfRocmVersionLessThan(version=None):
    def dec_fn(fn):
        @wraps(fn)
        def wrap_fn(self, *args, **kwargs):
            if self.device_type == "cuda":
                if not TEST_WITH_ROCM:
                    reason = "ROCm not available"
                    raise unittest.SkipTest(reason)
                rocm_version_tuple = _get_torch_rocm_version()
                if (
                    rocm_version_tuple is None
                    or version is None
                    or rocm_version_tuple < tuple(version)
                ):
                    reason = (
                        f"ROCm {rocm_version_tuple} is available but {version} required"
                    )
                    raise unittest.SkipTest(reason)

            return fn(self, *args, **kwargs)

        return wrap_fn

    return dec_fn

